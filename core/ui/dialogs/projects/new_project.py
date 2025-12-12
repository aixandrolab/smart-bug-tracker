from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QHBoxLayout,
    QPushButton,
    QFileDialog, 
    QMessageBox
)

import os

from core.models.project import Project
from core.utils.project_file_handler import ProjectFileHandler


class NewProjectDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New project")
        self.setFixedSize(400, 450)
        self.project_created = False
        self.created_project_path = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Project's title:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Example: MyAwesomeApp")
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Short description...")
        layout.addWidget(self.desc_input)
        
        layout.addWidget(QLabel("Author:"))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Your name")
        layout.addWidget(self.author_input)

        layout.addWidget(QLabel("GitHub Repository (optional):"))
        github_layout = QHBoxLayout()
        self.github_input = QLineEdit()
        self.github_input.setPlaceholderText("https://github.com/username/repository")
        github_layout.addWidget(self.github_input)
        
        template_btn = QPushButton("📋")
        template_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                padding: 0px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0097A7;
            }
            QPushButton:pressed {
                background-color: #006064;
            }
        """)
        template_btn.setMaximumWidth(50)
        template_btn.setToolTip("Insert template")
        template_btn.clicked.connect(self._insert_github_template)
        github_layout.addWidget(template_btn)
        
        layout.addLayout(github_layout)
        
        layout.addWidget(QLabel("Save as:"))
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Choose folder...")
        self.browse_btn = QPushButton("Review...")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                padding: 0px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0097A7;
            }
            QPushButton:pressed {
                background-color: #006064;
            }
        """)
        self.browse_btn.clicked.connect(self._browse_folder)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create")
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 0px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:pressed {
                background-color: #1B5E20;
            }
        """)
        self.cancel_btn = QPushButton("Back")
        
        self.create_btn.clicked.connect(self._create_project)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.create_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _insert_github_template(self):
        self.github_input.setText("https://github.com/username/repository")
    
    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Choose folder"
        )
        if folder:
            self.path_input.setText(folder)
    
    def _create_project(self):
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        author = self.author_input.text().strip()
        folder = self.path_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Input project's title")
            return
        
        if not folder:
            QMessageBox.warning(self, "Error", "Choose folder")
            return

        if github_url and not github_url.startswith(('http://', 'https://')):
            github_url = 'https://' + github_url
        
        project = Project(name, description, author)

        project.github_url = github_url
        
        filename = f"{name.replace(' ', '_')}.bugtracker.json"
        filepath = os.path.join(folder, filename)
        
        if ProjectFileHandler.save_project(project, filepath):
            self.project_created = True
            self.created_project_path = filepath
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Couldn't save project")
