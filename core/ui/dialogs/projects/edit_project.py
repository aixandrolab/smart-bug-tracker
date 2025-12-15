from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox
)
from PyQt5.QtMultimedia import QSound

from core.models.project import Project


class EditProjectDialog(QDialog):
    
    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Project")
        self.setFixedSize(800, 600)
        self.project = project

        self.click_sound = QSound('core/data/sounds/click.wav')
        self.error_sound = QSound('core/data/sounds/error.wav')
        
        self._setup_ui()
        self._load_project_data()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Project Name:*"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name...")
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Project description...")
        layout.addWidget(self.desc_input)
        
        layout.addWidget(QLabel("Author:*"))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Project author...")
        layout.addWidget(self.author_input)
        
        layout.addWidget(QLabel("GitHub Repository URL (optional):"))
        self.github_input = QLineEdit()
        self.github_input.setPlaceholderText("https://github.com/username/repository")
        layout.addWidget(self.github_input)
        
        layout.addWidget(QLabel("Versions (comma-separated):"))
        self.versions_input = QLineEdit()
        self.versions_input.setPlaceholderText("v1.0.0, v1.1.0, v2.0.0")
        layout.addWidget(self.versions_input)
        
        layout.addWidget(QLabel("Developers (comma-separated):"))
        self.developers_input = QLineEdit()
        self.developers_input.setPlaceholderText("developer1, developer2, developer3")
        layout.addWidget(self.developers_input)
        
        layout.addWidget(QLabel("Testers (comma-separated):"))
        self.testers_input = QLineEdit()
        self.testers_input.setPlaceholderText("tester1, tester2, tester3")
        layout.addWidget(self.testers_input)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Changes")
        
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
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

        self.save_btn.clicked.connect(self.on_click)

        self.cancel_btn = QPushButton("Cancel")

        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
        """)
        
        self.save_btn.clicked.connect(self._save_changes)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _load_project_data(self):
        self.name_input.setText(self.project.name)
        self.desc_input.setPlainText(self.project.description)
        self.author_input.setText(self.project.author)
        self.github_input.setText(self.project.github_url)
        
        if self.project.versions:
            self.versions_input.setText(", ".join(self.project.versions))
        
        if self.project.developers:
            self.developers_input.setText(", ".join(self.project.developers))
        
        if self.project.testers:
            self.testers_input.setText(", ".join(self.project.testers))
    
    def _save_changes(self):
        name = self.name_input.text().strip()
        author = self.author_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Project name is required!")
            return
        
        if not author:
            QMessageBox.warning(self, "Error", "Author is required!")
            return
        
        versions_text = self.versions_input.text().strip()
        versions = []
        if versions_text:
            versions = [v.strip() for v in versions_text.split(",") if v.strip()]
        
        developers_text = self.developers_input.text().strip()
        developers = []
        if developers_text:
            developers = [d.strip() for d in developers_text.split(",") if d.strip()]
        
        testers_text = self.testers_input.text().strip()
        testers = []
        if testers_text:
            testers = [t.strip() for t in testers_text.split(",") if t.strip()]
        
        self.project._name = name
        self.project._description = self.desc_input.toPlainText().strip()
        self.project._author = author
        self.project._github_url = self.github_input.text().strip()
        self.project._versions = versions
        self.project._developers = developers
        self.project._testers = testers
        
        self.accept()
    
    def get_updated_project(self):
        return self.project
    
    def on_click(self):
        self.click_sound.play()
    
    def on_notify(self):
        self.notify_sound.play()
    
    def on_error(self):
        self.error_sound.play()