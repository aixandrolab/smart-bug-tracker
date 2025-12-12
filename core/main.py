from typing import List

from core.bug import Bug, BugPriority, BugStatus
from core.bug_detailed_window import BugDetailWindow
from core.bug_manager import BugManager
from core.project import Project
from core.project_file_handler import ProjectFileHandler

import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.task import Task, TaskPriority, TaskStatus
from core.task_detail_window import TaskDetailWindow
from core.task_manager import TaskManager


class RoleSelectionDialog(QDialog):
    
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Role")
        self.setFixedSize(400, 300)
        self.selected_role = None
        self.project_name = project_name
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header_label = QLabel(f"Select role for working with:\n {self.project_name}")
        header_label.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #0d6efd;")

        header_label.setMaximumWidth(380)

        layout.addWidget(header_label)
        
        layout.addSpacing(20)
        
        developer_btn = QPushButton("👨‍💻 Developer")
        developer_btn.setMinimumHeight(60)
        developer_btn.clicked.connect(lambda: self._select_role("developer"))
        developer_btn.setToolTip("Can create test tasks, view bugs, manage project versions")
        layout.addWidget(developer_btn)
        
        tester_btn = QPushButton("🧪 Tester")
        tester_btn.setMinimumHeight(60)
        tester_btn.clicked.connect(lambda: self._select_role("tester"))
        tester_btn.setToolTip("Can add bugs, execute test cases")
        layout.addWidget(tester_btn)
        
        layout.addStretch()
        
        desc_label = QLabel("Role can be changed later in project settings")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #888888;")
        layout.addWidget(desc_label)
        
        self.setLayout(layout)
    
    def _select_role(self, role):
        self.selected_role = role
        self.accept()

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

class DeveloperWindow(QMainWindow):
    
    def __init__(self, project, filepath, parent=None):
        super().__init__(parent)
        self.project = project
        self.filepath = filepath
        
        self.task_manager = None
        self.bug_manager = None
        self.current_version = ""
        self.showMaximized() 
        
        self.project_data = ProjectFileHandler.load_project_full(filepath)
        if not self.project_data:
            QMessageBox.critical(self, "Error", "Failed to load project data")
            self.close()
            return
        
        self.setWindowTitle(f"Smart Bug Tracker - {project.name} [Developer]")
        self.setGeometry(100, 100, 1200, 800)
        
        self._setup_ui()
        self._setup_menu()
        self._setup_shortcuts()
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)
        
        export_action = QAction("Export JSON", self)
        export_action.triggered.connect(self._export_json)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        project_menu = menubar.addMenu("Project")

        github_action = QAction("🌐 Open GitHub Repository", self)
        github_action.triggered.connect(self._open_github)
        project_menu.addAction(github_action)
        
        copy_url_action = QAction("📋 Copy GitHub URL", self)
        copy_url_action.triggered.connect(self._copy_github_url)
        project_menu.addAction(copy_url_action)
        
        project_menu.addSeparator()
        
        update_github_action = QAction("⚙️ Update GitHub URL", self)
        update_github_action.triggered.connect(self._update_github_url)
        project_menu.addAction(update_github_action)
        
        version_action = QAction("Manage Versions", self)
        version_action.triggered.connect(self._manage_versions)
        project_menu.addAction(version_action)
        
        view_menu = menubar.addMenu("View")
        
        show_all_action = QAction("Show All Tasks", self)
        show_all_action.triggered.connect(self._show_all_tasks)
        view_menu.addAction(show_all_action)
        
        show_critical_action = QAction("Show Critical Only", self)
        show_critical_action.triggered.connect(lambda: self._filter_by_priority("Critical"))
        view_menu.addAction(show_critical_action)
        
        show_high_action = QAction("Show High Priority", self)
        show_high_action.triggered.connect(lambda: self._filter_by_priority("High"))
        view_menu.addAction(show_high_action)

        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("About", self)
        help_action.triggered.connect(self._show_about)
        help_menu.addAction(help_action)

        help_shortcuts_action = QAction("Shortcuts help", self)
        help_shortcuts_action.triggered.connect(self._show_help)
        help_menu.addAction(help_shortcuts_action)
    
    def _setup_shortcuts(self):
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(lambda: self.search_input.setFocus())
        
        clear_shortcut = QShortcut(QKeySequence("Ctrl+Shift+F"), self)
        clear_shortcut.activated.connect(self._clear_filters)
        
        critical_shortcut = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        critical_shortcut.activated.connect(lambda: self._filter_by_priority("Critical"))
        
        all_shortcut = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        all_shortcut.activated.connect(self._show_all_tasks)
        
        export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_shortcut.activated.connect(self._export_json)
        
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self._save_project)
        
        new_task_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_task_shortcut.activated.connect(self._add_test_task)
        
        delete_task_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_task_shortcut.activated.connect(self._delete_selected_task)
        
        mark_bug_fixed_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        mark_bug_fixed_shortcut.activated.connect(
            lambda: self._mark_selected_bug_status(BugStatus.FIXED)
        )
        
        mark_bug_in_progress_shortcut = QShortcut(QKeySequence("Ctrl+Shift+P"), self)
        mark_bug_in_progress_shortcut.activated.connect(
            lambda: self._mark_selected_bug_status(BugStatus.IN_PROGRESS)
        )
        
        edit_task_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        edit_task_shortcut.activated.connect(self._edit_selected_task)
        
        refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        refresh_shortcut.activated.connect(self._refresh_data)
        
        tasks_tab_shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        tasks_tab_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(0))
        
        bugs_tab_shortcut = QShortcut(QKeySequence("Ctrl+2"), self)
        bugs_tab_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(1))
        
        stats_tab_shortcut = QShortcut(QKeySequence("Ctrl+3"), self)
        stats_tab_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(2))
        
        mark_done_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        mark_done_shortcut.activated.connect(lambda: self._mark_selected_task_status(TaskStatus.DONE))
        
        mark_in_progress_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        mark_in_progress_shortcut.activated.connect(lambda: self._mark_selected_task_status(TaskStatus.IN_PROGRESS))
        
        github_shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        github_shortcut.activated.connect(self._open_github)
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        header_layout = QHBoxLayout()
        
        project_label = QLabel(f"📁 Project: {self.project.name}")
        project_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        header_layout.addWidget(project_label)
        
        header_layout.addStretch()
        
        mode_label = QLabel("🛠️ Developer")
        mode_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 0px 12px;
                border-radius: 4px;
                border: 1px solid white;
            }
        """)
        header_layout.addWidget(mode_label)
        
        main_layout.addLayout(header_layout)

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
        main_layout.addWidget(line)
        
        top_panel = self._create_top_panel()
        main_layout.addLayout(top_panel)
        
        main_layout.addSpacing(10)
        
        self.tab_widget = QTabWidget()
        
        self.tasks_tab = self._create_tasks_tab()
        self.tab_widget.addTab(self.tasks_tab, "📋 Tasks")
        
        self.bugs_tab = self._create_bugs_tab()
        self.tab_widget.addTab(self.bugs_tab, "🐛 Bugs")
        
        self.stats_tab = self._create_stats_tab()
        self.tab_widget.addTab(self.stats_tab, "📊 Statistics")
        
        main_layout.addWidget(self.tab_widget)
        
        self.statusBar().showMessage(f"Project: {self.project.name} | Developer Mode")
    
    def _create_top_panel(self):
        layout = QHBoxLayout()

        version_label = QLabel("Version:")
        layout.addWidget(version_label)
        
        self.version_combo = QComboBox()
        self.version_combo.addItem("Select version...")
        
        for version in self.project.versions:
            self.version_combo.addItem(version)
        
        self.version_combo.currentTextChanged.connect(self._on_version_changed)
        layout.addWidget(self.version_combo)
        
        new_version_btn = QPushButton("➕ New Version")
        new_version_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 0px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        new_version_btn.clicked.connect(self._create_new_version)
        layout.addWidget(new_version_btn)

        layout.addStretch()

        new_task_btn = QPushButton("📝 Add Test Task")
        new_task_btn.setStyleSheet("""
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
        new_task_btn.clicked.connect(self._add_test_task)
        layout.addWidget(new_task_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
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
        refresh_btn.clicked.connect(self._refresh_data)
        layout.addWidget(refresh_btn)
        
        return layout
    
    def _create_tasks_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()

        filter_panel = QHBoxLayout()

        filter_panel.addWidget(QLabel("Filter:"))
        self.filter_priority_combo = QComboBox()
        self.filter_priority_combo.addItems(["All", "Critical", "High", "Medium", "Low"])
        self.filter_priority_combo.currentTextChanged.connect(self._apply_filters)
        filter_panel.addWidget(self.filter_priority_combo)
        
        self.filter_status_combo = QComboBox()
        self.filter_status_combo.addItems([
            "All Statuses",
            "Todo",
            "In Progress", 
            "Ready for Test",
            "Testing",
            "Done",
            "Blocked"
        ])
        self.filter_status_combo.currentTextChanged.connect(self._apply_filters)
        filter_panel.addWidget(self.filter_status_combo)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.setMaximumWidth(200)
        self.search_input.textChanged.connect(self._apply_filters)
        filter_panel.addWidget(self.search_input)
        
        clear_filters_btn = QPushButton("Clear Filters")
        clear_filters_btn.setStyleSheet("""
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
        clear_filters_btn.clicked.connect(self._clear_filters)
        clear_filters_btn.setMaximumWidth(120)
        clear_filters_btn.setToolTip("Clear all filters (Ctrl+Shift+F)")
        filter_panel.addWidget(clear_filters_btn)

        filter_panel.addStretch()
        main_layout.addLayout(filter_panel)
        
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(5)
        self.tasks_table.setHorizontalHeaderLabels(["ID", "Title", "Priority", "Status", "Bugs"])
        self.tasks_table.horizontalHeader().setStretchLastSection(True)
        self.tasks_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.tasks_table.itemDoubleClicked.connect(self._on_task_double_clicked)
        
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self._show_tasks_context_menu)
        
        main_layout.addWidget(self.tasks_table)
        
        widget.setLayout(main_layout)
        return widget
    
    def _create_bugs_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        filter_panel = QHBoxLayout()
        
        filter_panel.addWidget(QLabel("Filter:"))
        
        self.bug_filter_status = QComboBox()
        self.bug_filter_status.addItems(["All Statuses", "Open", "In Progress", "Fixed", "Won't Fix", "Duplicate", "Invalid"])
        self.bug_filter_status.currentTextChanged.connect(self._refresh_bugs_table)
        filter_panel.addWidget(self.bug_filter_status)
        
        self.bug_filter_priority = QComboBox()
        self.bug_filter_priority.addItems(["All Priorities", "Critical", "High", "Medium", "Low"])
        self.bug_filter_priority.currentTextChanged.connect(self._refresh_bugs_table)
        filter_panel.addWidget(self.bug_filter_priority)
        
        self.bug_search_input = QLineEdit()
        self.bug_search_input.setPlaceholderText("Search bugs...")
        self.bug_search_input.textChanged.connect(self._refresh_bugs_table)
        filter_panel.addWidget(self.bug_search_input)
        
        clear_bug_filters_btn = QPushButton("Clear Filters")
        clear_bug_filters_btn.setStyleSheet("""
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
        clear_bug_filters_btn.clicked.connect(self._clear_bug_filters)
        filter_panel.addWidget(clear_bug_filters_btn)
        
        filter_panel.addStretch()
        main_layout.addLayout(filter_panel)
        
        self.bugs_table = QTableWidget()
        self.bugs_table.setColumnCount(6)
        self.bugs_table.setHorizontalHeaderLabels(["ID", "Title", "Priority", "Status", "Task", "Date"])
        self.bugs_table.horizontalHeader().setStretchLastSection(True)
        self.bugs_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.bugs_table.itemDoubleClicked.connect(self._on_bug_double_clicked)
        
        self.bugs_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bugs_table.customContextMenuRequested.connect(self._show_bugs_context_menu)
        
        main_layout.addWidget(self.bugs_table)
        
        widget.setLayout(main_layout)
        return widget
    
    def _create_stats_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        task_stats_group = QGroupBox("Task Statistics")
        task_stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #0d6efd;
                border: 2px solid #123262;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        task_stats_layout = QVBoxLayout()
        
        self.total_tasks_label = QLabel("Total Tasks: 0")
        task_stats_layout.addWidget(self.total_tasks_label)
        
        self.todo_tasks_label = QLabel("Todo Tasks: 0")
        task_stats_layout.addWidget(self.todo_tasks_label)
        
        self.in_progress_tasks_label = QLabel("In Progress Tasks: 0")
        task_stats_layout.addWidget(self.in_progress_tasks_label)
        
        self.critical_tasks_label = QLabel("Critical Tasks: 0")
        task_stats_layout.addWidget(self.critical_tasks_label)
        
        self.status_stats_label = QLabel()
        task_stats_layout.addWidget(self.status_stats_label)
        
        task_stats_group.setLayout(task_stats_layout)
        layout.addWidget(task_stats_group)
        
        bug_stats_group = QGroupBox("Bug Statistics")
        bug_stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: #0d6efd;
                border: 2px solid #123262;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        bug_stats_layout = QVBoxLayout()
        
        self.total_bugs_label = QLabel("Total Bugs: 0")
        bug_stats_layout.addWidget(self.total_bugs_label)
        
        self.open_bugs_label = QLabel("Open Bugs: 0")
        bug_stats_layout.addWidget(self.open_bugs_label)
        
        self.fixed_bugs_label = QLabel("Fixed Bugs: 0")
        bug_stats_layout.addWidget(self.fixed_bugs_label)
        
        self.critical_bugs_label = QLabel("Critical Bugs: 0")
        bug_stats_layout.addWidget(self.critical_bugs_label)
        
        bug_stats_group.setLayout(bug_stats_layout)
        layout.addWidget(bug_stats_group)
        
        layout.addStretch()
        
        export_layout = QHBoxLayout()
        
        export_stats_btn = QPushButton("Export Statistics to JSON")
        export_stats_btn.clicked.connect(self._export_statistics)
        export_layout.addWidget(export_stats_btn)
        
        export_all_btn = QPushButton("Export Full Report")
        export_all_btn.clicked.connect(self._export_full_report)
        export_layout.addWidget(export_all_btn)
        
        layout.addLayout(export_layout)
        
        widget.setLayout(layout)
        return widget
    
    def _on_version_changed(self, version):
        if version != "Select version...":
            self.current_version = version
            self._load_version_data(version)
    
    def _load_version_data(self, version):
        self.current_version = version
        
        self.task_manager = TaskManager(self.project_data, version)
        self.bug_manager = BugManager(self.project_data, version)
        
        self._clear_filters()
        self._clear_bug_filters()
        
        self._apply_filters()
        self._refresh_bugs_table()
        self._update_statistics()
        
        self.statusBar().showMessage(
            f"Version: {version} | "
            f"Tasks: {self.task_manager.count} | "
            f"Bugs: {self.bug_manager.count} | "
            f"Open Bugs: {self.bug_manager.open_count}"
        )
    
    def _create_new_version(self):
        version_name, ok = QInputDialog.getText(
            self, 
            "New Version",
            "Enter version name (e.g., v1.2.0):"
        )
        
        if ok and version_name:
            if version_name not in self.project.versions:
                self.project.add_version(version_name)
                
                self.version_combo.addItem(version_name)
                self.version_combo.setCurrentText(version_name)
                
                self._save_project()
            else:
                QMessageBox.warning(self, "Error", "Version already exists!")
    
    def _apply_filters(self):
        if not self.task_manager:
            return
        
        priority_filter_text = self.filter_priority_combo.currentText()
        status_filter_text = self.filter_status_combo.currentText()
        search_text = self.search_input.text().strip()
        
        priority_map = {
            "Critical": TaskPriority.CRITICAL,
            "High": TaskPriority.HIGH,
            "Medium": TaskPriority.MEDIUM,
            "Low": TaskPriority.LOW
        }
        
        status_map = {
            "Todo": TaskStatus.TODO,
            "In Progress": TaskStatus.IN_PROGRESS,
            "Ready for Test": TaskStatus.READY_FOR_TEST,
            "Testing": TaskStatus.TESTING,
            "Done": TaskStatus.DONE,
            "Blocked": TaskStatus.BLOCKED
        }
        
        priority_filter = priority_map.get(priority_filter_text) if priority_filter_text != "All" else None
        status_filter = status_map.get(status_filter_text) if status_filter_text != "All Statuses" else None
        
        filtered_tasks = self.task_manager.filter_tasks(
            priority_filter=priority_filter,
            status_filter=status_filter,
            search_text=search_text
        )
        
        self._update_tasks_table(filtered_tasks)
        
        self._update_filter_status_bar(filtered_tasks, priority_filter_text, status_filter_text, search_text)
    
    def _update_tasks_table(self, tasks):
        self.tasks_table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            id_item = QTableWidgetItem(task.id)
            id_item.setData(Qt.UserRole, task.id)
            
            title_item = QTableWidgetItem(task.title)
            
            priority_item = QTableWidgetItem(task.priority.value.upper())
            
            status_item = QTableWidgetItem(task.status.value.replace('_', ' ').title())
            
            bugs_count = len(self.bug_manager.get_bugs_by_task(task.id)) if self.bug_manager else 0
            bugs_item = QTableWidgetItem(str(bugs_count))
            
            status_text = task.status.value.replace('_', ' ').title()
            
            status_color = task.get_status_color()
            status_item.setForeground(status_color)
            
            if task.status == TaskStatus.DONE:
                done_color = QColor(60, 150, 60, 30)
                for item in [id_item, title_item, priority_item, status_item, bugs_item]:
                    item.setBackground(done_color)
            
            if task.status == TaskStatus.IN_PROGRESS:
                font = QFont()
                font.setBold(True)
                title_item.setFont(font)
            elif task.status == TaskStatus.BLOCKED:
                font = QFont()
                font.setStrikeOut(True)
                title_item.setFont(font)
                title_item.setForeground(QColor(150, 150, 150))
            
            if task.priority == TaskPriority.CRITICAL:
                priority_item.setForeground(QColor(255, 100, 100))
            elif task.priority == TaskPriority.HIGH:
                priority_item.setForeground(QColor(255, 150, 50))
            elif task.priority == TaskPriority.MEDIUM:
                priority_item.setForeground(QColor(255, 200, 50))
            else:
                priority_item.setForeground(QColor(150, 200, 150))
            
            if task.priority == TaskPriority.CRITICAL:
                title_item.setText("🔥 " + title_item.text())
            elif task.priority == TaskPriority.HIGH:
                title_item.setText("⚠️ " + title_item.text())
            
            if task.status == TaskStatus.DONE:
                title_item.setText("✅ " + title_item.text())
            
            title_item.setToolTip(f"Status: {status_text}\nDescription: {task.description}")
            status_item.setToolTip(f"Click to change status")
            
            self.tasks_table.setItem(row, 0, id_item)
            self.tasks_table.setItem(row, 1, title_item)
            self.tasks_table.setItem(row, 2, priority_item)
            self.tasks_table.setItem(row, 3, status_item)
            self.tasks_table.setItem(row, 4, bugs_item)
        
        self.tasks_table.sortItems(3, Qt.AscendingOrder)
        
        self._update_task_count_label(len(tasks))
    
    def _update_filter_status_bar(self, filtered_tasks, priority_filter, status_filter, search_text):
        total_tasks = self.task_manager.count if self.task_manager else 0
        shown_tasks = len(filtered_tasks)
        
        filter_parts = []
        if priority_filter != "All":
            filter_parts.append(f"Priority={priority_filter}")
        if status_filter != "All Statuses":
            filter_parts.append(f"Status={status_filter}")
        if search_text:
            filter_parts.append(f"Search='{search_text}'")
        
        if filter_parts:
            filter_str = " | ".join(filter_parts)
            message = f"Showing {shown_tasks} of {total_tasks} tasks [{filter_str}]"
        else:
            message = f"Showing all {total_tasks} tasks"
        
        self.statusBar().showMessage(message, 5000)
    
    def _update_task_count_label(self, filtered_count: int = None):
        if not self.task_manager:
            return
        
        total_count = self.task_manager.count
        if filtered_count is None:
            filtered_count = total_count
        
        if filtered_count != total_count:
            header_text = f"Test Tasks ({filtered_count} of {total_count})"
        else:
            header_text = f"Test Tasks ({total_count})"
        
        self.setWindowTitle(f"Smart Bug Tracker - {self.project.name} [Developer] | {header_text}")
    
    def _clear_filters(self):
        if not self.task_manager:
            return
        
        self.filter_priority_combo.setCurrentText("All")
        self.filter_status_combo.setCurrentText("All Statuses")
        self.search_input.clear()
        
        all_tasks = self.task_manager.get_all_tasks()
        
        self._update_tasks_table(all_tasks)
        
        total_count = len(all_tasks)
        self.statusBar().showMessage(f"Cleared filters | Showing all {total_count} tasks", 3000)
        
        self._update_task_count_label(total_count)
    
    def _show_all_tasks(self):
        self._clear_filters()
    
    def _filter_by_priority(self, priority: str):
        self.filter_priority_combo.setCurrentText(priority)
        self._apply_filters()
    
    def _on_task_double_clicked(self, item):
        row = item.row()
        task_id_item = self.tasks_table.item(row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        
        if task:
            dialog = TaskDetailWindow(task, self)
            dialog.exec_()
    
    def _show_tasks_context_menu(self, position):
        if not self.task_manager:
            return
        
        menu = QMenu()
        
        edit_action = menu.addAction("✏️ Edit Task")
        view_action = menu.addAction("👁️ View Task Details")
        delete_action = menu.addAction("🗑️ Delete Task")
        menu.addSeparator()
        mark_in_progress = menu.addAction("🔄 Mark as In Progress")
        mark_done = menu.addAction("✅ Mark as Done")
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        if not task:
            return
        
        edit_action.triggered.connect(lambda: self._edit_task(task))
        view_action.triggered.connect(lambda: self._view_task_details(task))
        delete_action.triggered.connect(lambda: self._delete_task(task))
        mark_in_progress.triggered.connect(lambda: self._mark_task_status(task, TaskStatus.IN_PROGRESS))
        mark_done.triggered.connect(lambda: self._mark_task_status(task, TaskStatus.DONE))
        
        menu.exec_(self.tasks_table.viewport().mapToGlobal(position))
    
    def _view_task_details(self, task):
        dialog = TaskDetailWindow(task, self)
        dialog.exec_()
    
    def _add_test_task(self):
        if not self.current_version:
            QMessageBox.warning(self, "Error", "Select a version first!")
            return
        
        if not self.task_manager:
            QMessageBox.warning(self, "Error", "Task manager not initialized. Select version again.")
            return
        
        dialog = AddTaskDialog(self.current_version, self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            if task_data:
                task = self.task_manager.add_task(**task_data)
                if task:
                    self._apply_filters()
                    self._update_statistics()
                    
                    self._save_project()
                    
                    for row in range(self.tasks_table.rowCount()):
                        item = self.tasks_table.item(row, 0)
                        if item and item.text() == task.id:
                            self.tasks_table.selectRow(row)
                            break
                    
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"Task '{task.title}' added successfully!"
                    )
                else:
                    QMessageBox.warning(self, "Error", "Failed to add task")
    
    def _edit_task(self, task):
        dialog = EditTaskDialog(task, self)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_updated_task_data()
            if updated_data and self.task_manager.update_task(task.id, **updated_data):
                self._apply_filters()
                self._save_project()
                QMessageBox.information(self, "Success", "Task updated successfully!")
    
    def _delete_task(self, task):
        reply = QMessageBox.question(
            self,
            "Delete Task",
            f"Are you sure you want to delete task '{task.title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.task_manager.delete_task(task.id):
                self._apply_filters()
                self._update_statistics()
                self._save_project()
                QMessageBox.information(self, "Success", "Task deleted successfully!")
    
    def _mark_task_status(self, task, status: TaskStatus):
        if self.task_manager.update_task(task.id, status=status):
            self._apply_filters()
            self._save_project()
            status_text = status.value.replace('_', ' ').title()
            self.statusBar().showMessage(f"Task marked as {status_text}", 3000)
    
    def _refresh_bugs_table(self):
        if not self.bug_manager:
            self.bugs_table.setRowCount(0)
            return
        
        status_text = self.bug_filter_status.currentText()
        priority_text = self.bug_filter_priority.currentText()
        search_text = self.bug_search_input.text().strip()
        
        status_map = {
            "Open": BugStatus.OPEN,
            "In Progress": BugStatus.IN_PROGRESS,
            "Fixed": BugStatus.FIXED,
            "Won't Fix": BugStatus.WONT_FIX,
            "Duplicate": BugStatus.DUPLICATE,
            "Invalid": BugStatus.INVALID
        }
        
        priority_map = {
            "Critical": BugPriority.CRITICAL,
            "High": BugPriority.HIGH,
            "Medium": BugPriority.MEDIUM,
            "Low": BugPriority.LOW
        }
        
        status_filter = status_map.get(status_text) if status_text != "All Statuses" else None
        priority_filter = priority_map.get(priority_text) if priority_text != "All Priorities" else None
        
        bugs = self.bug_manager.filter_bugs(
            priority_filter=priority_filter,
            status_filter=status_filter,
            search_text=search_text
        )
        
        self.bugs_table.setRowCount(len(bugs))
        
        for row, bug in enumerate(bugs):
            id_item = QTableWidgetItem(bug.id)
            id_item.setData(Qt.UserRole, bug.id)
            self.bugs_table.setItem(row, 0, id_item)
            
            title_item = QTableWidgetItem(bug.title)
            self.bugs_table.setItem(row, 1, title_item)
            
            priority_item = QTableWidgetItem(bug.priority.value.upper())
            
            if bug.priority == BugPriority.CRITICAL:
                priority_item.setForeground(QColor(255, 100, 100))
            elif bug.priority == BugPriority.HIGH:
                priority_item.setForeground(QColor(255, 150, 50))
            elif bug.priority == BugPriority.MEDIUM:
                priority_item.setForeground(QColor(255, 200, 50))
            else:
                priority_item.setForeground(QColor(150, 200, 150))
            
            self.bugs_table.setItem(row, 2, priority_item)
            
            status_item = QTableWidgetItem(bug.status.value.replace('_', ' ').title())
            status_color = bug.get_status_color()
            status_item.setForeground(QColor(status_color))
            self.bugs_table.setItem(row, 3, status_item)
            
            task_item = QTableWidgetItem(bug.task_id if bug.task_id else "No task")
            self.bugs_table.setItem(row, 4, task_item)
            
            date_str = bug.created_at[:10]
            date_item = QTableWidgetItem(date_str)
            self.bugs_table.setItem(row, 5, date_item)
        
        self.bugs_table.sortItems(5, Qt.DescendingOrder)
    
    def _clear_bug_filters(self):
        self.bug_filter_status.setCurrentText("All Statuses")
        self.bug_filter_priority.setCurrentText("All Priorities")
        self.bug_search_input.clear()
        self._refresh_bugs_table()
    
    def _on_bug_double_clicked(self, item):
        row = item.row()
        bug_id_item = self.bugs_table.item(row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        
        if bug:
            dialog = BugDetailWindow(bug, self.task_manager, self)
            dialog.exec_()

    def _view_bug_details(self, bug):
        dialog = BugDetailWindow(bug, self.task_manager, self)
        dialog.exec_()

    
    def _show_bugs_context_menu(self, position):
        if not self.bug_manager:
            return
        
        menu = QMenu()
        
        selected_row = self.bugs_table.currentRow()
        if selected_row < 0:
            return
        
        bug_id_item = self.bugs_table.item(selected_row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        if not bug:
            return
        
        view_action = menu.addAction("👁️ View Bug Details")
        view_action.triggered.connect(lambda: self._view_bug_details(bug))
        
        edit_action = menu.addAction("✏️ Edit Bug")
        edit_action.triggered.connect(lambda: self._edit_bug_developer(bug))
        
        add_comment_action = menu.addAction("💬 Add Comment")
        add_comment_action.triggered.connect(lambda: self._add_bug_comment_dialog(bug))
        
        menu.addSeparator()
        
        if bug.status != BugStatus.FIXED:
            mark_fixed_action = menu.addAction("✅ Mark as Fixed")
            mark_fixed_action.triggered.connect(lambda: self._mark_bug_status(bug, BugStatus.FIXED))
        
        if bug.status != BugStatus.IN_PROGRESS:
            mark_in_progress_action = menu.addAction("🔄 Mark as In Progress")
            mark_in_progress_action.triggered.connect(lambda: self._mark_bug_status(bug, BugStatus.IN_PROGRESS))
                
        menu.exec_(self.bugs_table.viewport().mapToGlobal(position))
    
    def _edit_bug_developer(self, bug):
        if not self.task_manager or not self.bug_manager:
            return
        
        available_tasks = self.task_manager.get_all_tasks()
        
        dialog = EditBugDialog(bug, available_tasks, is_tester=False, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_updated_bug_data()
            if updated_data and self.bug_manager.update_bug(bug.id, **updated_data):
                self._refresh_bugs_table()
                self._save_project()
                self.statusBar().showMessage("Bug updated successfully!", 3000)
    
    def _mark_bug_status(self, bug, status: BugStatus):
        if self.bug_manager.update_bug(bug.id, status=status):
            self._refresh_bugs_table()
            self._save_project()
            status_text = status.value.replace('_', ' ').title()
            self.statusBar().showMessage(f"Bug marked as {status_text}", 3000)
    
    def _add_bug_comment_dialog(self, bug):
        comment, ok = QInputDialog.getMultiLineText(
            self,
            "Add Comment",
            "Enter your comment:",
            ""
        )
        
        if ok and comment.strip():
            author = "Developer"
            if self.bug_manager.add_comment(bug.id, author, comment.strip()):
                self._refresh_bugs_table()
                self._save_project()
                self.statusBar().showMessage("Comment added successfully!", 3000)
    
    def _update_statistics(self):
        if not self.task_manager or not self.bug_manager:
            self.total_tasks_label.setText("Total Tasks: 0")
            self.todo_tasks_label.setText("Todo Tasks: 0")
            self.in_progress_tasks_label.setText("In Progress Tasks: 0")
            self.critical_tasks_label.setText("Critical Tasks: 0")
            self.status_stats_label.setText("")
            
            self.total_bugs_label.setText("Total Bugs: 0")
            self.open_bugs_label.setText("Open Bugs: 0")
            self.fixed_bugs_label.setText("Fixed Bugs: 0")
            self.critical_bugs_label.setText("Critical Bugs: 0")
            return
        
        task_stats = self.task_manager.get_task_statistics()
        self.total_tasks_label.setText(f"Total Tasks: {task_stats['total']}")
        self.todo_tasks_label.setText(f"Todo Tasks: {task_stats['todo']}")
        self.in_progress_tasks_label.setText(f"In Progress Tasks: {task_stats['in_progress']}")
        self.critical_tasks_label.setText(f"Critical Tasks: {task_stats['critical']}")
        
        status_texts = []
        for status_value, count in task_stats['by_status'].items():
            if count > 0:
                status_name = status_value.replace('_', ' ').title()
                status_texts.append(f"{status_name}: {count}")
        
        if status_texts:
            self.status_stats_label.setText(" | ".join(status_texts))
        else:
            self.status_stats_label.setText("")
        
        bug_stats = self.bug_manager.get_bug_statistics()
        self.total_bugs_label.setText(f"Total Bugs: {bug_stats['total']}")
        self.open_bugs_label.setText(f"Open Bugs: {bug_stats['open']}")
        self.fixed_bugs_label.setText(f"Fixed Bugs: {bug_stats['fixed']}")
        self.critical_bugs_label.setText(f"Critical Bugs: {bug_stats['critical']}")
    
    def _save_project(self):
        versions_data = self.project_data.get("versions", {})
        
        if ProjectFileHandler.save_project(self.project, self.filepath, versions_data):
            self.statusBar().showMessage("Project saved successfully!", 3000)
            return True
        else:
            QMessageBox.warning(self, "Error", "Failed to save project")
            return False
    
    def _refresh_data(self):
        self.project_data = ProjectFileHandler.load_project_full(self.filepath)
        if not self.project_data:
            QMessageBox.warning(self, "Error", "Failed to reload project data")
            return
        
        if self.current_version:
            self.task_manager = TaskManager(self.project_data, self.current_version)
            self.bug_manager = BugManager(self.project_data, self.current_version)
            self._apply_filters()
            self._refresh_bugs_table()
            self._update_statistics()
            self.statusBar().showMessage("Data refreshed successfully!", 3000)
    
    def _export_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Project",
            f"{self.project.name}_export.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                versions_data = self.project_data.get("versions", {})
                success = ProjectFileHandler.save_project(self.project, file_path, versions_data)
                
                if success:
                    QMessageBox.information(self, "Success", f"Project exported to:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to export project")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def _export_statistics(self):
        if not self.task_manager or not self.bug_manager:
            QMessageBox.warning(self, "Error", "No data to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Statistics",
            f"{self.project.name}_stats.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                import json
                
                stats = {
                    "project": self.project.name,
                    "version": self.current_version,
                    "date": QDateTime.currentDateTime().toString(Qt.ISODate),
                    "task_statistics": self.task_manager.get_task_statistics(),
                    "bug_statistics": self.bug_manager.get_bug_statistics()
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=4, ensure_ascii=False)
                
                QMessageBox.information(self, "Success", f"Statistics exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def _export_full_report(self):
        if not self.task_manager or not self.bug_manager:
            QMessageBox.warning(self, "Error", "No data to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Full Report",
            f"{self.project.name}_report.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                import json
                
                report = {
                    "project": self.project.name,
                    "version": self.current_version,
                    "export_date": QDateTime.currentDateTime().toString(Qt.ISODate),
                    "tasks": {
                        task.id: task.to_dict() for task in self.task_manager.get_all_tasks()
                    },
                    "bugs": {
                        bug.id: bug.to_dict() for bug in self.bug_manager.get_all_bugs()
                    },
                    "statistics": {
                        "tasks": self.task_manager.get_task_statistics(),
                        "bugs": self.bug_manager.get_bug_statistics()
                    }
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=4, ensure_ascii=False)
                
                QMessageBox.information(self, "Success", f"Full report exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def _manage_versions(self):
        QMessageBox.information(self, "Info", "Version management - coming soon!")

    def _delete_selected_task(self):
        if not self.task_manager:
            return
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a task to delete")
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        
        if task:
            self._delete_task(task)

    def _edit_selected_task(self):
        if not self.task_manager:
            return
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a task to edit")
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        
        if task:
            self._edit_task(task)

    def _mark_selected_task_status(self, status: TaskStatus):
        if not self.task_manager:
            return
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a task")
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        
        if task:
            self._mark_task_status(task, status)
    
    def _mark_selected_bug_status(self, status: BugStatus):
        if not self.bug_manager:
            return
        
        selected_row = self.bugs_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a bug")
            return
        
        bug_id_item = self.bugs_table.item(selected_row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        
        if bug:
            self._mark_bug_status(bug, status)
    
    def _open_github(self):
        if not self.project.github_url:
            self._show_no_github_url_warning()
            return
        
        try:
            import webbrowser
            webbrowser.open(self.project.github_url)
            self.statusBar().showMessage(f"Opening GitHub: {self.project.github_url}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot open browser: {str(e)}")
    
    def _copy_github_url(self):
        if not self.project.github_url:
            self._show_no_github_url_warning()
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(self.project.github_url)
        self.statusBar().showMessage("GitHub URL copied to clipboard!", 3000)
    
    def _update_github_url(self):
        current_url = self.project.github_url
        new_url, ok = QInputDialog.getText(
            self,
            "Update GitHub URL",
            "Enter new GitHub repository URL:",
            QLineEdit.Normal,
            current_url
        )
        
        if ok:
            self.project.github_url = new_url.strip()
            self._save_project()
            
            if new_url:
                self.statusBar().showMessage("GitHub URL updated!", 3000)
            else:
                self.statusBar().showMessage("GitHub URL cleared!", 3000)
    
    def _show_no_github_url_warning(self):
        reply = QMessageBox.question(
            self,
            "No GitHub URL",
            "This project doesn't have a GitHub repository URL.\n"
            "Would you like to set it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            self._update_github_url()
    
    def _show_about(self):
        about_text = f"""
        <h2>Smart Bug Tracker</h2>
        <p>Version 1.0.0</p>
        <p>Comprehensive bug tracking and test management system</p>

        <hr>
        
        <h3>Current Project</h3>
        <p><b>Name:</b> {self.project.name}</p>
        <p><b>Author:</b> {self.project.author}</p>
        <p><b>GitHub:</b> {self.project.github_url if self.project.github_url else 'Not set'}</p>
        <p><b>Versions:</b> {', '.join(self.project.versions) if self.project.versions else 'None'}</p>
        
        <hr>
        <p>Copyright © 2025, Alexander Suvorov</p>
        <p><a href="https://github.com/aixandrolab/smart-bug-tracker">GitHub Repository</a></p>
        """
        
        QMessageBox.about(self, "About Smart Bug Tracker", about_text)

    def _show_help(self):
        help_text = """
        <h2>Developer Mode - Keyboard Shortcuts</h2>

        <hr>
        
        <h3>Navigation</h3>
        <p><b>Ctrl+1:</b> Tasks tab</p>
        <p><b>Ctrl+2:</b> Bugs tab</p>
        <p><b>Ctrl+3:</b> Statistics tab</p>
        <p><b>F5:</b> Refresh data</p>

        <hr>
        
        <h3>Tasks</h3>
        <p><b>Ctrl+T:</b> Add new task</p>
        <p><b>Ctrl+R:</b> Edit selected task</p>
        <p><b>Delete:</b> Delete selected task</p>
        <p><b>Ctrl+D:</b> Mark task as Done</p>
        <p><b>Ctrl+P:</b> Mark task as In Progress</p>
        
        <hr>
        
        <h3>Bugs</h3>
        <p><b>Ctrl+Shift+D:</b> Make bug as fixed</p>
        <p><b>Ctrl+Shift+P:</b> Make bug as in progress</p>
        
        <hr>

        <h3>Search & Filter</h3>
        <p><b>Ctrl+F:</b> Focus search</p>
        <p><b>Ctrl+Shift+F:</b> Clear filters</p>
        <p><b>Ctrl+Shift+C:</b> Filter critical tasks</p>
        <p><b>Ctrl+Shift+A:</b> Show all tasks</p>
        
        <hr>

        <h3>File Operations</h3>
        <p><b>Ctrl+S:</b> Save project</p>
        <p><b>Ctrl+E:</b> Export JSON</p>
        
        <hr>

        <h3>Other</h3>
        <p><b>Ctrl+G:</b> Open GitHub repository</p>
        """
        QMessageBox.about(self, "About Developer's shortcuts", help_text)


class AddTaskDialog(QDialog):    
    def __init__(self, version: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Test Task - {version}")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QLabel[title="true"] {
                color: #0d6efd;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        self.task_data = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Task Title:*"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title...")
        layout.addWidget(self.title_input)
        
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Task description...")
        layout.addWidget(self.desc_input)
        
        layout.addWidget(QLabel("Priority:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            "Critical", 
            "High", 
            "Medium", 
            "Low"
        ])
        layout.addWidget(self.priority_combo)
        
        layout.addWidget(QLabel("Test Instructions:"))
        self.instructions_input = QTextEdit()
        self.instructions_input.setMaximumHeight(100)
        self.instructions_input.setPlaceholderText("Instructions for testers...")
        layout.addWidget(self.instructions_input)
        
        layout.addWidget(QLabel("Assigned to (optional):"))
        self.assigned_input = QLineEdit()
        self.assigned_input.setPlaceholderText("Enter name...")
        layout.addWidget(self.assigned_input)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Task")
        self.cancel_btn = QPushButton("Cancel")
        
        self.add_btn.clicked.connect(self._add_task)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _add_task(self):
        title = self.title_input.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Task title is required!")
            return
        
        priority_map = {
            "Critical": TaskPriority.CRITICAL,
            "High": TaskPriority.HIGH,
            "Medium": TaskPriority.MEDIUM,
            "Low": TaskPriority.LOW
        }
        
        self.task_data = {
            "title": title,
            "description": self.desc_input.toPlainText().strip(),
            "priority": priority_map[self.priority_combo.currentText()],
            "test_instructions": self.instructions_input.toPlainText().strip(),
            "assigned_to": self.assigned_input.text().strip()
        }
        
        self.accept()
    
    def get_task_data(self):
        return self.task_data

class EditTaskDialog(QDialog):    
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Task - {task.id}")
        self.setFixedSize(500, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QLabel[title="true"] {
                color: #0d6efd;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        self.task = task
        self.updated_task_data = None
        
        self._setup_ui()
        self._load_task_data()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Task ID:"))
        id_label = QLabel(self.task.id)
        id_label.setStyleSheet("font-weight: bold; color: #888888;")
        layout.addWidget(id_label)
        
        layout.addWidget(QLabel("Task Title:*"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        layout.addWidget(self.desc_input)
        
        layout.addWidget(QLabel("Priority:"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            "Critical", 
            "High", 
            "Medium", 
            "Low"
        ])
        layout.addWidget(self.priority_combo)
        
        layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "Todo",
            "In Progress", 
            "Ready for Test",
            "Testing",
            "Done",
            "Blocked"
        ])
        layout.addWidget(self.status_combo)
        
        layout.addWidget(QLabel("Test Instructions:"))
        self.instructions_input = QTextEdit()
        self.instructions_input.setMaximumHeight(100)
        layout.addWidget(self.instructions_input)
        
        layout.addWidget(QLabel("Assigned to:"))
        self.assigned_input = QLineEdit()
        layout.addWidget(self.assigned_input)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Changes")
        self.cancel_btn = QPushButton("Cancel")
        
        self.save_btn.clicked.connect(self._save_changes)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _load_task_data(self):
        self.title_input.setText(self.task.title)
        self.desc_input.setPlainText(self.task.description)
        
        priority_index = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3
        }
        self.priority_combo.setCurrentIndex(
            priority_index.get(self.task.priority, 2)
        )
        
        status_index = {
            TaskStatus.TODO: 0,
            TaskStatus.IN_PROGRESS: 1,
            TaskStatus.READY_FOR_TEST: 2,
            TaskStatus.TESTING: 3,
            TaskStatus.DONE: 4,
            TaskStatus.BLOCKED: 5
        }
        self.status_combo.setCurrentIndex(
            status_index.get(self.task.status, 0)
        )
        
        self.instructions_input.setPlainText(self.task.test_instructions)
        self.assigned_input.setText(self.task.assigned_to)
    
    def _save_changes(self):
        title = self.title_input.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Task title is required!")
            return
        
        priority_map = {
            "Critical": TaskPriority.CRITICAL,
            "High": TaskPriority.HIGH,
            "Medium": TaskPriority.MEDIUM,
            "Low": TaskPriority.LOW
        }
        
        status_map = {
            "Todo": TaskStatus.TODO,
            "In Progress": TaskStatus.IN_PROGRESS,
            "Ready for Test": TaskStatus.READY_FOR_TEST,
            "Testing": TaskStatus.TESTING,
            "Done": TaskStatus.DONE,
            "Blocked": TaskStatus.BLOCKED
        }
        
        self.updated_task_data = {
            "title": title,
            "description": self.desc_input.toPlainText().strip(),
            "priority": priority_map[self.priority_combo.currentText()],
            "status": status_map[self.status_combo.currentText()],
            "test_instructions": self.instructions_input.toPlainText().strip(),
            "assigned_to": self.assigned_input.text().strip()
        }
        
        self.accept()
    
    def get_updated_task_data(self):
        return self.updated_task_data

class TesterWindow(QMainWindow):
    
    def __init__(self, project, filepath, parent=None):
        super().__init__(parent)
        self.project = project
        self.filepath = filepath
        
        self.task_manager = None
        self.bug_manager = None
        self.current_version = ""
        self.showMaximized() 
        
        self.project_data = ProjectFileHandler.load_project_full(filepath)
        if not self.project_data:
            QMessageBox.critical(self, "Error", "Failed to load project data")
            self.close()
            return
        
        self.setWindowTitle(f"Smart Bug Tracker - {project.name} [Tester]")
        self.setGeometry(100, 100, 1200, 800)
        
        self._setup_ui()
        self._setup_menu()
        self._setup_shortcuts()
    
    def _setup_shortcuts(self):
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self._save_project)
        
        export_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_shortcut.activated.connect(self._export_json)
        
        new_bug_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        new_bug_shortcut.activated.connect(self._add_bug)
        
        delete_bug_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_bug_shortcut.activated.connect(self._delete_selected_bug)
        
        delete_bug_alt_shortcut = QShortcut(QKeySequence("Ctrl+Delete"), self)
        delete_bug_alt_shortcut.activated.connect(self._delete_selected_bug)
        
        edit_bug_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        edit_bug_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        edit_bug_shortcut.activated.connect(self._edit_selected_bug)
        
        refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        refresh_shortcut.activated.connect(self._refresh_data)

        tasks_tab_shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        tasks_tab_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(0))
        
        bugs_tab_shortcut = QShortcut(QKeySequence("Ctrl+2"), self)
        bugs_tab_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(1))
        
        stats_tab_shortcut = QShortcut(QKeySequence("Ctrl+3"), self)
        stats_tab_shortcut.activated.connect(lambda: self.tab_widget.setCurrentIndex(2))
        
        mark_fixed_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        mark_fixed_shortcut.activated.connect(lambda: self._mark_selected_bug_status(BugStatus.FIXED))
        
        mark_in_progress_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        mark_in_progress_shortcut.activated.connect(lambda: self._mark_selected_bug_status(BugStatus.IN_PROGRESS))
        
        search_tasks_shortcut = QShortcut(QKeySequence("Ctrl+Shift+F"), self)
        search_tasks_shortcut.activated.connect(lambda: self.task_search_input.setFocus())
        
        search_bugs_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_bugs_shortcut.activated.connect(lambda: self.bug_search_input.setFocus())
        
        github_shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        github_shortcut.activated.connect(self._open_github)
        
        help_shortcut = QShortcut(QKeySequence("F1"), self)
        help_shortcut.activated.connect(self._show_help)
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)
        
        export_action = QAction("Export JSON", self)
        export_action.triggered.connect(self._export_json)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        view_menu = menubar.addMenu("View")
        
        show_tasks_action = QAction("Show Tasks View", self)
        show_tasks_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(show_tasks_action)
        
        show_bugs_action = QAction("Show Bugs View", self)
        show_bugs_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        view_menu.addAction(show_bugs_action)

        vcs_menu = menubar.addMenu("VCS")
        
        github_action = QAction("🌐 Open GitHub Repository", self)
        github_action.triggered.connect(self._open_github)
        vcs_menu.addAction(github_action)
        
        copy_url_action = QAction("📋 Copy GitHub URL", self)
        copy_url_action.triggered.connect(self._copy_github_url)
        vcs_menu.addAction(copy_url_action)
        
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("About", self)
        help_action.triggered.connect(self._show_about)
        help_menu.addAction(help_action)

        help_shortcuts_action = QAction("Shortcuts help", self)
        help_shortcuts_action.triggered.connect(self._show_help)
        help_menu.addAction(help_shortcuts_action)
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        header_layout = QHBoxLayout()

        project_label = QLabel(f"📁 Project: {self.project.name}")
        project_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        header_layout.addWidget(project_label)
        
        header_layout.addStretch()
        
        mode_label = QLabel("🧪 Tester")
        mode_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 0px 12px;
                border-radius: 4px;
                border: 1px solid white;
            }
        """)
        header_layout.addWidget(mode_label)
        
        main_layout.addLayout(header_layout)

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
        main_layout.addWidget(line)
        
        top_panel = self._create_top_panel()
        main_layout.addLayout(top_panel)
        
        main_layout.addSpacing(10)
        
        self.tab_widget = QTabWidget()
        
        self.tasks_tab = self._create_tasks_tab()
        self.tab_widget.addTab(self.tasks_tab, "📋 Tasks")
        
        self.bugs_tab = self._create_bugs_tab()
        self.tab_widget.addTab(self.bugs_tab, "🐛 Bugs")
        
        self.stats_tab = self._create_stats_tab()
        self.tab_widget.addTab(self.stats_tab, "📊 Statistics")
        
        main_layout.addWidget(self.tab_widget)
        
        self.statusBar().showMessage(f"Project: {self.project.name} | Tester Mode")
    
    def _create_top_panel(self):
        layout = QHBoxLayout()
        
        version_label = QLabel("Version:")
        layout.addWidget(version_label)
        
        self.version_combo = QComboBox()
        self.version_combo.addItem("Select version...")
        
        for version in self.project.versions:
            self.version_combo.addItem(version)
        
        self.version_combo.currentTextChanged.connect(self._on_version_changed)
        layout.addWidget(self.version_combo)
        
        layout.addStretch()
        
        new_bug_btn = QPushButton("➕ Add Bug")
        new_bug_btn.setStyleSheet("""
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
        new_bug_btn.clicked.connect(self._add_bug)
        layout.addWidget(new_bug_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
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
        refresh_btn.clicked.connect(self._refresh_data)
        layout.addWidget(refresh_btn)
        
        return layout
    
    def _create_tasks_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        filter_panel = QHBoxLayout()
        
        filter_panel.addWidget(QLabel("Filter:"))
        
        self.task_filter_status = QComboBox()
        self.task_filter_status.addItems([
            "All Statuses", 
            "Todo", 
            "In Progress", 
            "Done", 
            "Blocked"
        ])
        self.task_filter_status.currentTextChanged.connect(self._refresh_tasks_table)
        filter_panel.addWidget(self.task_filter_status)
        
        self.task_filter_priority = QComboBox()
        self.task_filter_priority.addItems([
            "All Priorities", 
            "Critical", 
            "High", 
            "Medium", 
            "Low"
        ])
        self.task_filter_priority.currentTextChanged.connect(self._refresh_tasks_table)
        filter_panel.addWidget(self.task_filter_priority)
        
        self.task_search_input = QLineEdit()
        self.task_search_input.setPlaceholderText("Search tasks...")
        self.task_search_input.textChanged.connect(self._refresh_tasks_table)
        filter_panel.addWidget(self.task_search_input)
        
        clear_filters_btn = QPushButton("Clear Filters")
        clear_filters_btn.setStyleSheet("""
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
        clear_filters_btn.clicked.connect(self._clear_task_filters)
        filter_panel.addWidget(clear_filters_btn)
        
        filter_panel.addStretch()
        main_layout.addLayout(filter_panel)
        
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(6)
        self.tasks_table.setHorizontalHeaderLabels([
            "ID", 
            "Title", 
            "Priority", 
            "Status", 
            "Bugs", 
            "Created"
        ])
        self.tasks_table.horizontalHeader().setStretchLastSection(True)
        self.tasks_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.tasks_table.itemDoubleClicked.connect(self._on_task_double_clicked)
        
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self._show_tasks_context_menu)
        
        main_layout.addWidget(self.tasks_table)
        
        widget.setLayout(main_layout)
        return widget
    
    def _create_bugs_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        filter_panel = QHBoxLayout()
        
        filter_panel.addWidget(QLabel("Filter:"))
        
        self.bug_filter_status = QComboBox()
        self.bug_filter_status.addItems(["All Statuses", "Open", "In Progress", "Fixed", "Won't Fix", "Duplicate", "Invalid"])
        self.bug_filter_status.currentTextChanged.connect(self._refresh_bugs_table)
        filter_panel.addWidget(self.bug_filter_status)
        
        self.bug_filter_priority = QComboBox()
        self.bug_filter_priority.addItems(["All Priorities", "Critical", "High", "Medium", "Low"])
        self.bug_filter_priority.currentTextChanged.connect(self._refresh_bugs_table)
        filter_panel.addWidget(self.bug_filter_priority)
        
        self.bug_search_input = QLineEdit()
        self.bug_search_input.setPlaceholderText("Search bugs...")
        self.bug_search_input.textChanged.connect(self._refresh_bugs_table)
        filter_panel.addWidget(self.bug_search_input)
        
        clear_bug_filters_btn = QPushButton("Clear Filters")
        clear_bug_filters_btn.setStyleSheet("""
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
        clear_bug_filters_btn.clicked.connect(self._clear_bug_filters)
        filter_panel.addWidget(clear_bug_filters_btn)
        
        filter_panel.addStretch()
        main_layout.addLayout(filter_panel)
        
        self.bugs_table = QTableWidget()
        self.bugs_table.setColumnCount(6)
        self.bugs_table.setHorizontalHeaderLabels(["ID", "Title", "Priority", "Status", "Task", "Date"])
        self.bugs_table.horizontalHeader().setStretchLastSection(True)
        self.bugs_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.bugs_table.itemDoubleClicked.connect(self._on_bug_double_clicked)
        
        self.bugs_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bugs_table.customContextMenuRequested.connect(self._show_bugs_context_menu)
        
        main_layout.addWidget(self.bugs_table)
        
        widget.setLayout(main_layout)
        return widget

    def _create_stats_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.total_tasks_label = QLabel("Total Tasks: 0")
        layout.addWidget(self.total_tasks_label)
        
        self.todo_tasks_label = QLabel("Todo Tasks: 0")
        layout.addWidget(self.todo_tasks_label)
        
        self.total_bugs_label = QLabel("Total Bugs: 0")
        layout.addWidget(self.total_bugs_label)
        
        self.open_bugs_label = QLabel("Open Bugs: 0")
        layout.addWidget(self.open_bugs_label)
        
        self.fixed_bugs_label = QLabel("Fixed Bugs: 0")
        layout.addWidget(self.fixed_bugs_label)
        
        self.critical_bugs_label = QLabel("Critical Bugs: 0")
        layout.addWidget(self.critical_bugs_label)
        
        layout.addStretch()
        
        export_stats_btn = QPushButton("Export Statistics to JSON")
        export_stats_btn.clicked.connect(self._export_statistics)
        layout.addWidget(export_stats_btn)
        
        widget.setLayout(layout)
        return widget
        
    def _on_version_changed(self, version):
        if version != "Select version...":
            self.current_version = version
            self._load_version_data(version)
    
    def _load_version_data(self, version):
        self.current_version = version
        
        self.task_manager = TaskManager(self.project_data, version)
        self.bug_manager = BugManager(self.project_data, version)
        
        self._clear_bug_filters()
        
        self._refresh_tasks_table()
        self._refresh_bugs_table()
        self._update_statistics()
        
        self.statusBar().showMessage(
            f"Version: {version} | "
            f"Tasks: {self.task_manager.count} | "
            f"Bugs: {self.bug_manager.count} | "
            f"Open Bugs: {self.bug_manager.open_count}"
        )

    def _on_task_double_clicked(self, item):
        row = item.row()
        task_id_item = self.tasks_table.item(row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        
        if task:
            dialog = TaskDetailWindow(task, self)
            dialog.exec_()
    
    def _refresh_tasks_table(self):
        if not self.task_manager:
            self.tasks_table.setRowCount(0)
            return
        
        status_text = self.task_filter_status.currentText()
        priority_text = self.task_filter_priority.currentText()
        search_text = self.task_search_input.text().strip()
        
        status_map = {
            "Todo": TaskStatus.TODO,
            "In Progress": TaskStatus.IN_PROGRESS,
            "Done": TaskStatus.DONE,
            "Blocked": TaskStatus.BLOCKED,
        }
        
        priority_map = {
            "Critical": TaskPriority.CRITICAL,
            "High": TaskPriority.HIGH,
            "Medium": TaskPriority.MEDIUM,
            "Low": TaskPriority.LOW
        }
        
        status_filter = status_map.get(status_text) if status_text != "All Statuses" else None
        priority_filter = priority_map.get(priority_text) if priority_text != "All Priorities" else None
        
        tasks = self.task_manager.filter_tasks(
            priority_filter=priority_filter,
            status_filter=status_filter,
            search_text=search_text
        )
        
        self.tasks_table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            id_item = QTableWidgetItem(task.id)
            id_item.setData(Qt.UserRole, task.id)
            self.tasks_table.setItem(row, 0, id_item)
            
            title_item = QTableWidgetItem(task.title)
            self.tasks_table.setItem(row, 1, title_item)
            
            priority_item = QTableWidgetItem(task.priority.value.upper())
            if task.priority == TaskPriority.CRITICAL:
                priority_item.setForeground(QColor(255, 100, 100))
            elif task.priority == TaskPriority.HIGH:
                priority_item.setForeground(QColor(255, 150, 50))
            elif task.priority == TaskPriority.MEDIUM:
                priority_item.setForeground(QColor(255, 200, 50))
            else:
                priority_item.setForeground(QColor(150, 200, 150))
            self.tasks_table.setItem(row, 2, priority_item)
            
            status_item = QTableWidgetItem(task.status.value.replace('_', ' ').title())
            self.tasks_table.setItem(row, 3, status_item)
            
            bugs_count = len(self.bug_manager.get_bugs_by_task(task.id)) if self.bug_manager else 0
            bugs_item = QTableWidgetItem(str(bugs_count))
            if bugs_count > 0:
                bugs_item.setForeground(QColor(255, 100, 100))
            self.tasks_table.setItem(row, 4, bugs_item)
            
            date_str = task.created_at[:10] if task.created_at else "N/A"
            date_item = QTableWidgetItem(date_str)
            self.tasks_table.setItem(row, 5, date_item)
        
        self.tasks_table.sortItems(5, Qt.DescendingOrder)
    
    def _clear_task_filters(self):
        self.task_filter_status.setCurrentText("All Statuses")
        self.task_filter_priority.setCurrentText("All Priorities")
        self.task_search_input.clear()
        self._refresh_tasks_table()

    def _on_bug_double_clicked(self, item):
        row = item.row()
        bug_id_item = self.bugs_table.item(row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        
        if bug:
            dialog = BugDetailWindow(bug, self.task_manager, self)
            dialog.exec_()
    
    def _view_bug_details(self, bug):
        dialog = BugDetailWindow(bug, self.task_manager, self)
        dialog.exec_()

    
        
    def _show_tasks_context_menu(self, position):
        if not self.task_manager:
            return
        
        menu = QMenu()
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        if not task:
            return
        
        view_action = menu.addAction("👁️ View Task Details")
        view_action.triggered.connect(lambda: self._view_task_details(task))
        
        add_bug_action = menu.addAction("➕ Add Bug for this Task")
        add_bug_action.triggered.connect(lambda: self._add_bug_for_task(task))
        
        bugs_count = len(self.bug_manager.get_bugs_by_task(task.id)) if self.bug_manager else 0
        if bugs_count > 0:
            view_bugs_action = menu.addAction(f"👁️ View {bugs_count} Bugs")
            view_bugs_action.triggered.connect(lambda: self._view_task_bugs(task))
        
        menu.addSeparator()
        
        if task.status != TaskStatus.IN_PROGRESS:
            mark_in_progress = menu.addAction("🔄 Mark as In Progress")
            mark_in_progress.triggered.connect(lambda: self._mark_task_status(task, TaskStatus.IN_PROGRESS))
        
        if task.status != TaskStatus.DONE:
            mark_done = menu.addAction("✅ Mark as Done")
            mark_done.triggered.connect(lambda: self._mark_task_status(task, TaskStatus.DONE))
        
        menu.exec_(self.tasks_table.viewport().mapToGlobal(position))
    
    def _view_task_details(self, task):
        dialog = TaskDetailWindow(task, self)
        dialog.exec_()
    
    def _mark_task_status(self, task, status: TaskStatus):
        if self.task_manager.update_task(task.id, status=status):
            self._refresh_tasks_table()
            self._save_project()
            status_text = status.value.replace('_', ' ').title()
            self.statusBar().showMessage(f"Task marked as {status_text}", 3000)
        
    def _refresh_bugs_table(self):
        if not self.bug_manager:
            self.bugs_table.setRowCount(0)
            return
        
        status_text = self.bug_filter_status.currentText()
        priority_text = self.bug_filter_priority.currentText()
        search_text = self.bug_search_input.text().strip()
        
        status_map = {
            "Open": BugStatus.OPEN,
            "In Progress": BugStatus.IN_PROGRESS,
            "Fixed": BugStatus.FIXED,
            "Won't Fix": BugStatus.WONT_FIX,
            "Duplicate": BugStatus.DUPLICATE,
            "Invalid": BugStatus.INVALID
        }
        
        priority_map = {
            "Critical": BugPriority.CRITICAL,
            "High": BugPriority.HIGH,
            "Medium": BugPriority.MEDIUM,
            "Low": BugPriority.LOW
        }
        
        status_filter = status_map.get(status_text) if status_text != "All Statuses" else None
        priority_filter = priority_map.get(priority_text) if priority_text != "All Priorities" else None

        bugs = self.bug_manager.filter_bugs(
            priority_filter=priority_filter,
            status_filter=status_filter,
            search_text=search_text
        )
        
        self.bugs_table.setRowCount(len(bugs))
        
        for row, bug in enumerate(bugs):
            id_item = QTableWidgetItem(bug.id)
            id_item.setData(Qt.UserRole, bug.id)
            self.bugs_table.setItem(row, 0, id_item)
            
            title_item = QTableWidgetItem(bug.title)
            self.bugs_table.setItem(row, 1, title_item)
            
            priority_item = QTableWidgetItem(bug.priority.value.upper())
            
            if bug.priority == BugPriority.CRITICAL:
                priority_item.setForeground(QColor(255, 100, 100))
            elif bug.priority == BugPriority.HIGH:
                priority_item.setForeground(QColor(255, 150, 50))
            elif bug.priority == BugPriority.MEDIUM:
                priority_item.setForeground(QColor(255, 200, 50))
            else:
                priority_item.setForeground(QColor(150, 200, 150))
            
            self.bugs_table.setItem(row, 2, priority_item)
            
            status_item = QTableWidgetItem(bug.status.value.replace('_', ' ').title())
            status_color = bug.get_status_color()
            status_item.setForeground(QColor(status_color))
            self.bugs_table.setItem(row, 3, status_item)
            
            task_item = QTableWidgetItem(bug.task_id if bug.task_id else "No task")
            self.bugs_table.setItem(row, 4, task_item)
            
            date_str = bug.created_at[:10]
            date_item = QTableWidgetItem(date_str)
            self.bugs_table.setItem(row, 5, date_item)
        
        self.bugs_table.sortItems(5, Qt.DescendingOrder)
    
    def _clear_bug_filters(self):
        self.bug_filter_status.setCurrentText("All Statuses")
        self.bug_filter_priority.setCurrentText("All Priorities")
        self.bug_search_input.clear()
        self._refresh_bugs_table()
    
    def _show_bugs_context_menu(self, position):
        if not self.bug_manager:
            return
        
        menu = QMenu()
        
        selected_row = self.bugs_table.currentRow()
        if selected_row < 0:
            return
        
        bug_id_item = self.bugs_table.item(selected_row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        if not bug:
            return
        
        view_action = menu.addAction("👁️ View Bug Details")
        view_action.triggered.connect(lambda: self._view_bug_details(bug))

        edit_action = menu.addAction("✏️ Edit Bug")
        edit_action.triggered.connect(lambda: self._edit_bug(bug))

        add_comment_action = menu.addAction("💬 Add Comment")
        add_comment_action.triggered.connect(lambda: self._add_bug_comment_dialog(bug))
        
        menu.addSeparator()
        
        if bug.status != BugStatus.FIXED:
            mark_fixed_action = menu.addAction("✅ Mark as Fixed")
            mark_fixed_action.triggered.connect(lambda: self._mark_bug_status(bug, BugStatus.FIXED))
        
        if bug.status != BugStatus.IN_PROGRESS:
            mark_in_progress_action = menu.addAction("🔄 Mark as In Progress")
            mark_in_progress_action.triggered.connect(lambda: self._mark_bug_status(bug, BugStatus.IN_PROGRESS))
        
        menu.addSeparator()
        
        delete_action = menu.addAction("🗑️ Delete Bug")
        delete_action.triggered.connect(lambda: self._delete_bug(bug))
        
        menu.exec_(self.bugs_table.viewport().mapToGlobal(position))

    def _add_bug_comment_dialog(self, bug):
        comment, ok = QInputDialog.getMultiLineText(
            self,
            "Add Comment",
            "Enter your comment:",
            ""
        )
        
        if ok and comment.strip():
            author = "Tester"
            if self.bug_manager.add_comment(bug.id, author, comment.strip()):
                self._refresh_bugs_table()
                self._save_project()
                self.statusBar().showMessage("Comment added successfully!", 3000)
    
    def _add_bug(self):
        if not self.current_version:
            QMessageBox.warning(self, "Error", "Select a version first!")
            return
        
        if not self.task_manager or not self.bug_manager:
            QMessageBox.warning(self, "Error", "Managers not initialized!")
            return
        
        available_tasks = self.task_manager.get_all_tasks()
        
        dialog = AddBugDialog(self.current_version, available_tasks, self)
        if dialog.exec_() == QDialog.Accepted:
            bug_data = dialog.get_bug_data()
            if bug_data:
                bug = self.bug_manager.add_bug(**bug_data)
                if bug:
                    self._refresh_bugs_table()
                    self._refresh_tasks_table()
                    self._update_statistics()
                    self._save_project()
                    
                    self.tab_widget.setCurrentIndex(1)
                    
                    for row in range(self.bugs_table.rowCount()):
                        item = self.bugs_table.item(row, 0)
                        if item and item.text() == bug.id:
                            self.bugs_table.selectRow(row)
                            break
                    
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"Bug '{bug.title}' added successfully!"
                    )
                else:
                    QMessageBox.warning(self, "Error", "Failed to add bug")
    
    def _add_bug_for_task(self, task):
        if not self.current_version:
            QMessageBox.warning(self, "Error", "Select a version first!")
            return
        
        if not self.task_manager or not self.bug_manager:
            QMessageBox.warning(self, "Error", "Managers not initialized!")
            return
        
        available_tasks = [task]
        
        dialog = AddBugDialog(self.current_version, available_tasks, self)
        
        for i in range(dialog.task_combo.count()):
            if dialog.task_combo.itemData(i) == task.id:
                dialog.task_combo.setCurrentIndex(i)
                break
        
        if dialog.exec_() == QDialog.Accepted:
            bug_data = dialog.get_bug_data()
            if bug_data:
                bug = self.bug_manager.add_bug(**bug_data)
                if bug:
                    self._refresh_bugs_table()
                    self._refresh_tasks_table()
                    self._update_statistics()
                    self._save_project()
                    
                    self.tab_widget.setCurrentIndex(1)
                    
                    for row in range(self.bugs_table.rowCount()):
                        item = self.bugs_table.item(row, 0)
                        if item and item.text() == bug.id:
                            self.bugs_table.selectRow(row)
                            break
                    
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"Bug '{bug.title}' added for task '{task.title}'!"
                    )
                else:
                    QMessageBox.warning(self, "Error", "Failed to add bug")
    
    def _edit_bug(self, bug):
        if not self.task_manager or not self.bug_manager:
            return
        
        available_tasks = self.task_manager.get_all_tasks()
        
        dialog = EditBugDialog(bug, available_tasks, is_tester=True, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_updated_bug_data()
            if updated_data and self.bug_manager.update_bug(bug.id, **updated_data):
                self._refresh_bugs_table()
                self._save_project()
                self.statusBar().showMessage("Bug updated successfully!", 3000)
    
    def _mark_bug_status(self, bug, status: BugStatus):
        if self.bug_manager.update_bug(bug.id, status=status):
            self._refresh_bugs_table()
            self._save_project()
            status_text = status.value.replace('_', ' ').title()
            self.statusBar().showMessage(f"Bug marked as {status_text}", 3000)
    
    def _delete_bug(self, bug):
        reply = QMessageBox.question(
            self,
            "Delete Bug",
            f"Are you sure you want to delete bug '{bug.title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.bug_manager.delete_bug(bug.id):
                self._refresh_bugs_table()
                self._refresh_tasks_table()
                self._update_statistics()
                self._save_project()
                self.statusBar().showMessage("Bug deleted successfully!", 3000)
    
    def _view_task_bugs(self, task):
        if not self.bug_manager:
            return
        
        bugs = self.bug_manager.get_bugs_by_task(task.id)
        if bugs:
            self.tab_widget.setCurrentIndex(1)
            self.bug_search_input.setText(task.id)
        else:
            QMessageBox.information(self, "Info", f"No bugs found for task {task.id}")
    
    def _update_statistics(self):
        if not self.task_manager or not self.bug_manager:
            self.total_tasks_label.setText("Total Tasks: 0")
            self.todo_tasks_label.setText("Todo Tasks: 0")
            self.total_bugs_label.setText("Total Bugs: 0")
            self.open_bugs_label.setText("Open Bugs: 0")
            self.fixed_bugs_label.setText("Fixed Bugs: 0")
            self.critical_bugs_label.setText("Critical Bugs: 0")
            return
        
        task_stats = self.task_manager.get_task_statistics()
        self.total_tasks_label.setText(f"Total Tasks: {task_stats['total']}")
        self.todo_tasks_label.setText(f"Todo Tasks: {task_stats['todo']}")
        
        bug_stats = self.bug_manager.get_bug_statistics()
        self.total_bugs_label.setText(f"Total Bugs: {bug_stats['total']}")
        self.open_bugs_label.setText(f"Open Bugs: {bug_stats['open']}")
        self.fixed_bugs_label.setText(f"Fixed Bugs: {bug_stats['fixed']}")
        self.critical_bugs_label.setText(f"Critical Bugs: {bug_stats['critical']}")
    
    def _save_project(self):
        versions_data = self.project_data.get("versions", {})
        
        if ProjectFileHandler.save_project(self.project, self.filepath, versions_data):
            self.statusBar().showMessage("Project saved successfully!", 3000)
            return True
        else:
            QMessageBox.warning(self, "Error", "Failed to save project")
            return False
    
    def _refresh_data(self):
        self.project_data = ProjectFileHandler.load_project_full(self.filepath)
        if not self.project_data:
            QMessageBox.warning(self, "Error", "Failed to reload project data")
            return
        
        if self.current_version:
            self.task_manager = TaskManager(self.project_data, self.current_version)
            self.bug_manager = BugManager(self.project_data, self.current_version)
            self._refresh_tasks_table()
            self._refresh_bugs_table()
            self._update_statistics()
            self.statusBar().showMessage("Data refreshed successfully!", 3000)
    
    def _export_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Project",
            f"{self.project.name}_export.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                versions_data = self.project_data.get("versions", {})
                success = ProjectFileHandler.save_project(self.project, file_path, versions_data)
                
                if success:
                    QMessageBox.information(self, "Success", f"Project exported to:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to export project")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def _export_statistics(self):
        if not self.task_manager or not self.bug_manager:
            QMessageBox.warning(self, "Error", "No data to export")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Statistics",
            f"{self.project.name}_stats.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                import json
                
                stats = {
                    "project": self.project.name,
                    "version": self.current_version,
                    "date": QDateTime.currentDateTime().toString(Qt.ISODate),
                    "task_statistics": self.task_manager.get_task_statistics(),
                    "bug_statistics": self.bug_manager.get_bug_statistics()
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=4, ensure_ascii=False)
                
                QMessageBox.information(self, "Success", f"Statistics exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")

    def _delete_selected_bug(self):
        if not self.bug_manager:
            return
        
        selected_row = self.bugs_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a bug to delete")
            return
        
        bug_id_item = self.bugs_table.item(selected_row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        
        if bug:
            self._delete_bug(bug)

    def _edit_selected_bug(self):
        if not self.bug_manager:
            return
        
        selected_row = self.bugs_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a bug to edit")
            return
        
        bug_id_item = self.bugs_table.item(selected_row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        
        if bug:
            self._edit_bug(bug)

    def _mark_selected_bug_status(self, status: BugStatus):
        if not self.bug_manager:
            return
        
        selected_row = self.bugs_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a bug")
            return
        
        bug_id_item = self.bugs_table.item(selected_row, 0)
        if not bug_id_item:
            return
        
        bug_id = bug_id_item.data(Qt.UserRole)
        bug = self.bug_manager.get_bug(bug_id)
        
        if bug:
            self._mark_bug_status(bug, status)
    
    def _open_github(self):
        if not self.project.github_url:
            self._show_no_github_url_warning()
            return
            
        try:
            import webbrowser
            webbrowser.open(self.project.github_url)
            self.statusBar().showMessage(f"Opening GitHub: {self.project.github_url}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot open browser: {str(e)}")
    
    def _copy_github_url(self):
        if not self.project.github_url:
            self._show_no_github_url_warning()
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(self.project.github_url)
        self.statusBar().showMessage("GitHub URL copied to clipboard!", 3000)
    
    def _update_github_url(self):
        current_url = self.project.github_url
        new_url, ok = QInputDialog.getText(
            self,
            "Update GitHub URL",
            "Enter new GitHub repository URL:",
            QLineEdit.Normal,
            current_url
        )
        
        if ok:
            self.project.github_url = new_url.strip()
            self._save_project()
            
            if new_url:
                self.statusBar().showMessage("GitHub URL updated!", 3000)
            else:
                self.statusBar().showMessage("GitHub URL cleared!", 3000)
    
    def _show_no_github_url_warning(self):
        reply = QMessageBox.question(
            self,
            "No GitHub URL",
            "This project doesn't have a GitHub repository URL.\n"
            "Would you like to set it now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            self._update_github_url()
    
    def _show_about(self):
        about_text = f"""
        <h2>Smart Bug Tracker</h2>
        <p>Version 1.0.0</p>
        <p>Comprehensive bug tracking and test management system</p>

        <hr>
        
        <h3>Current Project</h3>
        <p><b>Name:</b> {self.project.name}</p>
        <p><b>Author:</b> {self.project.author}</p>
        <p><b>GitHub:</b> {self.project.github_url if self.project.github_url else 'Not set'}</p>
        <p><b>Versions:</b> {', '.join(self.project.versions) if self.project.versions else 'None'}</p>
        
        <hr>
        <p>Copyright © 2025, Alexander Suvorov</p>
        <p><a href="https://github.com/aixandrolab/smart-bug-tracker">GitHub Repository</a></p>
        """
        
        QMessageBox.about(self, "About Smart Bug Tracker", about_text)
    
    def _show_help(self):
        help_text = """
        <h2>Tester Mode - Keyboard Shortcuts</h2>

        <hr>
        
        <h3>Navigation</h3>
        <p><b>Ctrl+1:</b> Tasks tab</p>
        <p><b>Ctrl+2:</b> Bugs tab</p>
        <p><b>Ctrl+3:</b> Statistics tab</p>
        <p><b>F5:</b> Refresh data</p>

        <hr>
        
        <h3>Bugs</h3>
        <p><b>Ctrl+B:</b> Add new bug</p>
        <p><b>Ctrl+R:</b> Edit selected bug</p>
        <p><b>Delete:</b> Delete selected bug</p>
        <p><b>Ctrl+Delete:</b> Delete selected bug (alternative)</p>
        <p><b>Ctrl+D:</b> Mark bug as Fixed</p>
        <p><b>Ctrl+P:</b> Mark bug as In Progress</p>

        <hr>
        
        <h3>Search</h3>
        <p><b>Ctrl+F:</b> Focus bug search</p>
        <p><b>Ctrl+Shift+F:</b> Focus task search</p>

        <hr>
        
        <h3>File Operations</h3>
        <p><b>Ctrl+S:</b> Save project</p>
        <p><b>Ctrl+E:</b> Export JSON</p>

        <hr>
        
        <h3>Other</h3>
        <p><b>Ctrl+G:</b> Open GitHub repository</p>
        <p><b>F1:</b> Show this help</p>
        """
        QMessageBox.about(self, "About Tester's shortcuts", help_text)

class AddBugDialog(QDialog):
    bug_added = pyqtSignal()
    def __init__(self, version: str, available_tasks: List[Task], parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Bug - {version}")
        self.setFixedSize(600, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QLabel[title="true"] {
                color: #0d6efd;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        self.available_tasks = available_tasks
        self.bug_data = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        scroll_layout.addWidget(QLabel("Bug Title:*"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Short descriptive title...")
        scroll_layout.addWidget(self.title_input)
        
        scroll_layout.addWidget(QLabel("Description:*"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("Detailed description of the bug...")
        scroll_layout.addWidget(self.desc_input)
        
        scroll_layout.addWidget(QLabel("Associated Task:"))
        self.task_combo = QComboBox()
        self.task_combo.addItem("No task (general bug)")
        
        for task in self.available_tasks:
            display_text = f"{task.id}: {task.title}"
            self.task_combo.addItem(display_text)
            self.task_combo.setItemData(self.task_combo.count() - 1, task.id)
        
        scroll_layout.addWidget(self.task_combo)
        
        scroll_layout.addWidget(QLabel("Priority:*"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            "Critical (Blocks development/testing)",
            "High (Major issue, needs immediate attention)",
            "Medium (Should be fixed soon)",
            "Low (Minor issue, can be fixed later)"
        ])
        scroll_layout.addWidget(self.priority_combo)
        
        scroll_layout.addWidget(QLabel("Steps to Reproduce:"))
        self.steps_input = QTextEdit()
        self.steps_input.setMaximumHeight(120)
        self.steps_input.setPlaceholderText("1. Go to...\n2. Click on...\n3. Observe...")
        scroll_layout.addWidget(self.steps_input)
        
        results_layout = QHBoxLayout()
        
        expected_widget = QWidget()
        expected_layout = QVBoxLayout()
        expected_layout.addWidget(QLabel("Expected Result:"))
        self.expected_input = QTextEdit()
        self.expected_input.setMaximumHeight(80)
        self.expected_input.setPlaceholderText("What should happen...")
        expected_layout.addWidget(self.expected_input)
        expected_widget.setLayout(expected_layout)
        results_layout.addWidget(expected_widget)
        
        actual_widget = QWidget()
        actual_layout = QVBoxLayout()
        actual_layout.addWidget(QLabel("Actual Result:"))
        self.actual_input = QTextEdit()
        self.actual_input.setMaximumHeight(80)
        self.actual_input.setPlaceholderText("What actually happens...")
        actual_layout.addWidget(self.actual_input)
        actual_widget.setLayout(actual_layout)
        results_layout.addWidget(actual_widget)
        
        scroll_layout.addLayout(results_layout)
        
        scroll_layout.addWidget(QLabel("Screenshot:"))
        screenshot_layout = QHBoxLayout()
        self.screenshot_path_input = QLineEdit()
        self.screenshot_path_input.setPlaceholderText("Path to screenshot image...")
        screenshot_layout.addWidget(self.screenshot_path_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_screenshot)
        screenshot_layout.addWidget(browse_btn)
        
        scroll_layout.addLayout(screenshot_layout)
        
        scroll_layout.addWidget(QLabel("Reported by:"))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Your name")
        scroll_layout.addWidget(self.author_input)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Bug")
        self.cancel_btn = QPushButton("Cancel")
        
        self.add_btn.clicked.connect(self._add_bug)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _browse_screenshot(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Screenshot",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if file_path:
            self.screenshot_path_input.setText(file_path)
    
    def _add_bug(self):
        title = self.title_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Bug title is required!")
            return
        
        if not description:
            QMessageBox.warning(self, "Error", "Bug description is required!")
            return
        
        task_id = ""
        if self.task_combo.currentIndex() > 0:
            task_id = self.task_combo.currentData()
        
        priority_text = self.priority_combo.currentText()
        priority_map = {
            "Critical (Blocks development/testing)": BugPriority.CRITICAL,
            "High (Major issue, needs immediate attention)": BugPriority.HIGH,
            "Medium (Should be fixed soon)": BugPriority.MEDIUM,
            "Low (Minor issue, can be fixed later)": BugPriority.LOW
        }
        
        self.bug_data = {
            "title": title,
            "description": description,
            "priority": priority_map[priority_text],
            "task_id": task_id,
            "steps_to_reproduce": self.steps_input.toPlainText().strip(),
            "expected_result": self.expected_input.toPlainText().strip(),
            "actual_result": self.actual_input.toPlainText().strip(),
            "screenshot_path": self.screenshot_path_input.text().strip(),
            "author": self.author_input.text().strip()
        }
        
        self.accept()
    
    def get_bug_data(self):
        return self.bug_data


class EditBugDialog(QDialog):    
    def __init__(self, bug: Bug, available_tasks: List[Task], is_tester: bool = True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Bug - {bug.id}")
        self.setFixedSize(600, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QLabel[title="true"] {
                color: #0d6efd;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        self.bug = bug
        self.available_tasks = available_tasks
        self.is_tester = is_tester
        self.updated_bug_data = None
        
        self._setup_ui()
        self._load_bug_data()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        scroll_layout.addWidget(QLabel("Bug ID:"))
        id_label = QLabel(self.bug.id)
        id_label.setStyleSheet("font-weight: bold; color: #888888;")
        scroll_layout.addWidget(id_label)
        
        scroll_layout.addWidget(QLabel("Bug Title:*"))
        self.title_input = QLineEdit()
        scroll_layout.addWidget(self.title_input)
        
        scroll_layout.addWidget(QLabel("Description:*"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        scroll_layout.addWidget(self.desc_input)
        
        scroll_layout.addWidget(QLabel("Associated Task:"))
        self.task_combo = QComboBox()
        self.task_combo.addItem("No task (general bug)")
        
        for task in self.available_tasks:
            display_text = f"{task.id}: {task.title}"
            self.task_combo.addItem(display_text)
            self.task_combo.setItemData(self.task_combo.count() - 1, task.id)
        
        scroll_layout.addWidget(self.task_combo)
        
        scroll_layout.addWidget(QLabel("Priority:*"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            "Critical (Blocks development/testing)",
            "High (Major issue, needs immediate attention)",
            "Medium (Should be fixed soon)",
            "Low (Minor issue, can be fixed later)"
        ])
        scroll_layout.addWidget(self.priority_combo)
        
        if self.is_tester:
            scroll_layout.addWidget(QLabel("Status:"))
            self.status_combo = QComboBox()
            self.status_combo.addItems([
                "Open",
                "In Progress",
                "Fixed",
                "Won't Fix",
                "Duplicate",
                "Invalid"
            ])
            scroll_layout.addWidget(self.status_combo)
        
        scroll_layout.addWidget(QLabel("Steps to Reproduce:"))
        self.steps_input = QTextEdit()
        self.steps_input.setMaximumHeight(120)
        scroll_layout.addWidget(self.steps_input)
        
        results_layout = QHBoxLayout()
        
        expected_widget = QWidget()
        expected_layout = QVBoxLayout()
        expected_layout.addWidget(QLabel("Expected Result:"))
        self.expected_input = QTextEdit()
        self.expected_input.setMaximumHeight(80)
        expected_layout.addWidget(self.expected_input)
        expected_widget.setLayout(expected_layout)
        results_layout.addWidget(expected_widget)
        
        actual_widget = QWidget()
        actual_layout = QVBoxLayout()
        actual_layout.addWidget(QLabel("Actual Result:"))
        self.actual_input = QTextEdit()
        self.actual_input.setMaximumHeight(80)
        actual_layout.addWidget(self.actual_input)
        actual_widget.setLayout(actual_layout)
        results_layout.addWidget(actual_widget)
        
        scroll_layout.addLayout(results_layout)
        
        scroll_layout.addWidget(QLabel("Screenshot:"))
        screenshot_layout = QHBoxLayout()
        self.screenshot_path_input = QLineEdit()
        screenshot_layout.addWidget(self.screenshot_path_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_screenshot)
        screenshot_layout.addWidget(browse_btn)
        
        scroll_layout.addLayout(screenshot_layout)
        
        if not self.is_tester:
            scroll_layout.addWidget(QLabel("Assigned to:"))
            self.assigned_input = QLineEdit()
            self.assigned_input.setPlaceholderText("Developer name")
            scroll_layout.addWidget(self.assigned_input)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Changes")
        self.cancel_btn = QPushButton("Cancel")
        
        self.save_btn.clicked.connect(self._save_changes)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _load_bug_data(self):
        self.title_input.setText(self.bug.title)
        self.desc_input.setPlainText(self.bug.description)
        
        if self.bug.task_id:
            for i in range(self.task_combo.count()):
                if self.task_combo.itemData(i) == self.bug.task_id:
                    self.task_combo.setCurrentIndex(i)
                    break
        
        priority_map = {
            BugPriority.CRITICAL: 0,
            BugPriority.HIGH: 1,
            BugPriority.MEDIUM: 2,
            BugPriority.LOW: 3
        }
        self.priority_combo.setCurrentIndex(
            priority_map.get(self.bug.priority, 2)
        )
        
        if self.is_tester:
            status_map = {
                BugStatus.OPEN: 0,
                BugStatus.IN_PROGRESS: 1,
                BugStatus.FIXED: 2,
                BugStatus.WONT_FIX: 3,
                BugStatus.DUPLICATE: 4,
                BugStatus.INVALID: 5
            }
            self.status_combo.setCurrentIndex(
                status_map.get(self.bug.status, 0)
            )
        
        self.steps_input.setPlainText(self.bug.steps_to_reproduce)
        self.expected_input.setPlainText(self.bug.expected_result)
        self.actual_input.setPlainText(self.bug.actual_result)
        self.screenshot_path_input.setText(self.bug.screenshot_path)
        
        if not self.is_tester:
            self.assigned_input.setText(self.bug.assigned_to)
    
    def _browse_screenshot(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Screenshot",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if file_path:
            self.screenshot_path_input.setText(file_path)
    
    def _save_changes(self):
        title = self.title_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Error", "Bug title is required!")
            return
        
        if not description:
            QMessageBox.warning(self, "Error", "Bug description is required!")
            return
        
        task_id = ""
        if self.task_combo.currentIndex() > 0:
            task_id = self.task_combo.currentData()
        
        priority_text = self.priority_combo.currentText().split(" (")[0]
        priority_map = {
            "Critical": BugPriority.CRITICAL,
            "High": BugPriority.HIGH,
            "Medium": BugPriority.MEDIUM,
            "Low": BugPriority.LOW
        }
        
        self.updated_bug_data = {
            "title": title,
            "description": description,
            "priority": priority_map[priority_text],
            "task_id": task_id,
            "steps_to_reproduce": self.steps_input.toPlainText().strip(),
            "expected_result": self.expected_input.toPlainText().strip(),
            "actual_result": self.actual_input.toPlainText().strip(),
            "screenshot_path": self.screenshot_path_input.text().strip()
        }
        
        if self.is_tester:
            status_map = {
                "Open": BugStatus.OPEN,
                "In Progress": BugStatus.IN_PROGRESS,
                "Fixed": BugStatus.FIXED,
                "Won't Fix": BugStatus.WONT_FIX,
                "Duplicate": BugStatus.DUPLICATE,
                "Invalid": BugStatus.INVALID
            }
            self.updated_bug_data["status"] = status_map[self.status_combo.currentText()]
        
        if not self.is_tester:
            self.updated_bug_data["assigned_to"] = self.assigned_input.text().strip()
        
        self.accept()
    
    def get_updated_bug_data(self):
        return self.updated_bug_data