from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QDialog, QFileDialog, QLineEdit, QTextEdit, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.project import Project
from core.project_file_handler import ProjectFileHandler

import os


class OpenProjectDialog(QFileDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open project")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter("Smart Bug Tracker (*.bugtracker.json)")
        self.setViewMode(QFileDialog.Detail)
        
        self.setDirectory(os.path.expanduser("~"))

class NewProjectDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New project")
        self.setFixedSize(400, 300)
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
        
        layout.addWidget(QLabel("Save as:"))
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Choose folder...")
        self.browse_btn = QPushButton("Review...")
        self.browse_btn.clicked.connect(self._browse_folder)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.create_btn = QPushButton("Создать")
        self.cancel_btn = QPushButton("Отмена")
        
        self.create_btn.clicked.connect(self._create_project)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.create_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
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
        
        project = Project(name, description, author)
        
        filename = f"{name.replace(' ', '_')}.bugtracker.json"
        filepath = os.path.join(folder, filename)
        
        if ProjectFileHandler.save_project(project, filepath):
            self.project_created = True
            self.created_project_path = filepath
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Couldn't save project")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Smart Bug Tracker')
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        title_label = QLabel("Smart Bug Tracker")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        desc_label = QLabel("Smart Bug Tracker")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addSpacing(40)
        
        btn_layout = QVBoxLayout()
        
        self.btn_new = QPushButton("+ New Project")
        self.btn_new.clicked.connect(self.on_new_project)
        btn_layout.addWidget(self.btn_new)
        
        self.btn_open = QPushButton("Open Project")
        self.btn_open.clicked.connect(self.on_open_project)
        btn_layout.addWidget(self.btn_open)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        bottom_layout = QHBoxLayout()
        
        self.btn_help = QPushButton("❓ HELP")
        self.btn_help.clicked.connect(self.on_help)
        bottom_layout.addWidget(self.btn_help)
        
        bottom_layout.addStretch()
        
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.clicked.connect(self.close)
        bottom_layout.addWidget(self.btn_exit)
        
        layout.addLayout(bottom_layout)

        self.center_window()

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
    
    def on_new_project(self):
        dialog = NewProjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self._load_project(dialog.created_project_path)
    
    def on_open_project(self):
        dialog = OpenProjectDialog(self)
        if dialog.exec_():
            files = dialog.selectedFiles()
            if files:
                self._load_project(files[0])
    
    def _load_project(self, filepath: str):
        project = ProjectFileHandler.load_project(filepath)
        if project:
            self.current_project = project
            self.current_filepath = filepath
            self.setWindowTitle(f"Smart Bug Tracker - {project.name}")
            QMessageBox.information(
                self, 
                "Prject successfully load",
                f"Project '{project.name}' successfully load!\n"
                f"Author: {project.author}\n"
                f"Versions: {len(project.versions)}"
            )
        else:
            QMessageBox.warning(self, "Error", "Cannot load project")
    
    def on_help(self):
        QMessageBox.information(
            self,
            'Smart Bug Tracker Help',
            '📂 <a href="https://github.com/aixandrolab/smart-bug-tracker" style="color: #2a82da;">GitHub Repository</a><br>'
        )
