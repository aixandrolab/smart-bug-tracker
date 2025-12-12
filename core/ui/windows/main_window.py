from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QDialog,
    QDesktopWidget,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.ui.dialogs.projects.new_project import NewProjectDialog
from core.ui.dialogs.projects.open_project import OpenProjectDialog
from core.ui.dialogs.roles.role_selection import RoleSelectionDialog
from core.ui.windows.developer_window import DeveloperWindow
from core.ui.windows.tester_window import TesterWindow
from core.utils.project_file_handler import ProjectFileHandler


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('Smart Bug Tracker')
        self.setGeometry(400, 400, 400, 350)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

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
        title_label.setStyleSheet("color: #0d6efd;")
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        desc_label = QLabel("Smart Bug Tracker is a comprehensive desktop application built with Python and PyQt5 that enables efficient bug tracking," \
        " test management, and project organization.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addSpacing(40)
        
        btn_layout = QVBoxLayout()
        
        self.btn_new = QPushButton("+ New Project")
        self.btn_new.setStyleSheet("""
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
        self.btn_new.clicked.connect(self.on_new_project)
        btn_layout.addWidget(self.btn_new)
        
        self.btn_open = QPushButton("Open Project")
        self.btn_open.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                padding: 0px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {style="color: #2a82da; text-decoration: none;"
                background-color: #0097A7;
            }
            QPushButton:pressed {
                background-color: #006064;
            }
        """)
        self.btn_open.clicked.connect(self.on_open_project)
        btn_layout.addWidget(self.btn_open)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        bottom_layout = QHBoxLayout()
        
        self.btn_help = QPushButton("❓ FAQ")
        self.btn_help.setStyleSheet("""
            QPushButton {
                background-color: #FFEB3B;
                color: #212121;
                border: none;
                padding: 0px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FDD835;
            }
            QPushButton:pressed {
                background-color: #FBC02D;
            }
        """)
        self.btn_help.clicked.connect(self.on_help)
        bottom_layout.addWidget(self.btn_help)
        
        bottom_layout.addStretch()
        
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                padding: 0px 16px;
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
        self.btn_exit.clicked.connect(self.close)
        bottom_layout.addWidget(self.btn_exit)
        
        layout.addLayout(bottom_layout)

        layout.addStretch()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("""
            QFrame {
                color: #00BCD4;
                margin-top: 5px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(line)

        copyright_text = 'Copyright © 2025, <a href="https://github.com/aixandrolab" style="color: #2a82da; text-decoration: none;">Alexander Suvorov</a>. All rights reserved.'
        copyright_label = QLabel(copyright_text)
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setWordWrap(True)
        copyright_label.setOpenExternalLinks(True)
        layout.addWidget(copyright_label)

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
            
            role_dialog = RoleSelectionDialog(project_name=project.name, parent=self)
            if role_dialog.exec_() == QDialog.Accepted:
                role = role_dialog.selected_role
                
                if role == "developer":
                    self.developer_window = DeveloperWindow(project, filepath, self)
                    self.developer_window.show()
                    self.hide()
                    
                elif role == "tester":
                    self.tester_window = TesterWindow(project, filepath, self)
                    self.tester_window.show()
                    self.hide()
            else:
                QMessageBox.warning(self, "Error", "Failed to load project")
    
    def on_help(self):
        help_text = """
        <h2>Smart Bug Tracker FAQ</h2>

        <hr>
        
        <h3>Quick Start</h3>
        <p>1. <b>Create New Project</b> - Start a new bug tracking project</p>
        <p>2. <b>Open Project</b> - Load an existing project file (.bugtracker.json)</p>
        <p>3. <b>Select Role</b> - Choose Developer or Tester mode</p>
        
        <h3>Features</h3>
        <p>• <b>Developer Mode:</b> Create tasks, manage bugs, track versions</p>
        <p>• <b>Tester Mode:</b> Execute tests, report bugs, add comments</p>
        <p>• <b>GitHub Integration:</b> Link projects to GitHub repositories</p>
        
        <h3>Keyboard Shortcuts</h3>
        <p>• <b>Ctrl+S:</b> Save project</p>
        <p>• <b>Ctrl+E:</b> Export to JSON</p>
        <p>• <b>Ctrl+F:</b> Search</p>
        
        <hr>
        <p><a href="https://github.com/aixandrolab/smart-bug-tracker" style="color: #2a82da; text-decoration: none;">GitHub Repository</a></p>
        <p>For support and issues, visit our GitHub page.</p>
        """
        
        QMessageBox.information(self, 'Smart Bug Tracker Help', help_text)
