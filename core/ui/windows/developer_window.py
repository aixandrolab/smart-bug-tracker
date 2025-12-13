from PyQt5.QtWidgets import (
    QMainWindow, 
    QMessageBox,
    QShortcut, 
    QVBoxLayout, 
    QAction, 
    QWidget, 
    QHBoxLayout, 
    QLabel, 
    QFrame, 
    QTabWidget,
    QComboBox,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QGroupBox,
    QInputDialog,
    QTableWidgetItem,
    QMenu,
    QDialog,
    QFileDialog,
    QApplication,
    QScrollArea,
    QGridLayout,
    QProgressBar
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QKeySequence, QColor, QFont

from core.managers.bug_manager import BugManager
from core.managers.task_manager import TaskManager
from core.models.bug import BugPriority, BugStatus
from core.models.task import TaskPriority, TaskStatus
from core.ui.windows.bug_detailed_window import BugDetailWindow
from core.ui.windows.task_detail_window import TaskDetailWindow
from core.ui.dialogs.bugs.edit_bug import EditBugDialog
from core.ui.dialogs.tasks.add_task import AddTaskDialog
from core.ui.dialogs.tasks.edit_task import EditTaskDialog
from core.utils.project_file_handler import ProjectFileHandler
from core.utils.statistics_generator import StatisticsGenerator


class DeveloperWindow(QMainWindow):
    
    def __init__(self, project, filepath, parent=None):
        super().__init__(parent)
        self.project = project
        self.filepath = filepath

        self.selected_task_id = None
        self.selected_bug_id = None
        
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

        switch_to_tester_action = QAction("🧪 Switch to Tester Mode", self)
        switch_to_tester_action.triggered.connect(self._switch_to_tester_mode)
        project_menu.addAction(switch_to_tester_action)

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
        
        show_tasks_action = QAction("Show Tasks Tab", self)
        show_tasks_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(show_tasks_action)
        
        show_bugs_action = QAction("Show Bugs Tab", self)
        show_bugs_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        view_menu.addAction(show_bugs_action)

        show_bugs_action = QAction("Show Stats Tab", self)
        show_bugs_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        view_menu.addAction(show_bugs_action)

        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("About", self)
        help_action.triggered.connect(self._show_about)
        help_menu.addAction(help_action)

        help_shortcuts_action = QAction("Help", self)
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
        header_layout.addWidget(refresh_btn)
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
        filter_panel.addWidget(new_task_btn)

        main_layout.addLayout(filter_panel)
        
        self.tasks_table = QTableWidget()
        self.tasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["Title", "Description","Priority", "Status", "Bugs", "ID", "Actions"])
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
        self.bugs_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bugs_table.setColumnCount(7)
        self.bugs_table.setHorizontalHeaderLabels(["Title", "Priority", "Status", "Task", "Date", "ID", "Actions"])
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
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        
        task_progress_group = QGroupBox("Task Completion")
        task_progress_layout = QVBoxLayout()
        task_progress_layout.setSpacing(5)
        self.simple_task_progress_bar = QProgressBar()
        self.simple_task_progress_bar.setRange(0, 100)
        self.simple_task_progress_bar.setValue(0)
        self.simple_task_progress_bar.setFormat("%p%")
        task_progress_layout.addWidget(self.simple_task_progress_bar)
        self.simple_task_percent = QLabel("0%")
        self.simple_task_percent.setAlignment(Qt.AlignCenter)
        task_progress_layout.addWidget(self.simple_task_percent)
        task_progress_group.setLayout(task_progress_layout)
        progress_layout.addWidget(task_progress_group)
        
        bug_progress_group = QGroupBox("Bug Resolution")
        bug_progress_layout = QVBoxLayout()
        bug_progress_layout.setSpacing(5)
        self.simple_bug_progress_bar = QProgressBar()
        self.simple_bug_progress_bar.setRange(0, 100)
        self.simple_bug_progress_bar.setValue(0)
        self.simple_bug_progress_bar.setFormat("%p%")
        bug_progress_layout.addWidget(self.simple_bug_progress_bar)
        self.simple_bug_percent = QLabel("0%")
        self.simple_bug_percent.setAlignment(Qt.AlignCenter)
        bug_progress_layout.addWidget(self.simple_bug_percent)
        bug_progress_group.setLayout(bug_progress_layout)
        progress_layout.addWidget(bug_progress_group)
        
        progress_layout.setStretch(0, 1)
        progress_layout.setStretch(1, 1)
        
        main_layout.addLayout(progress_layout)
        
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line1)
        
        stats_scroll = QScrollArea()
        stats_scroll.setWidgetResizable(True)
        stats_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        stats_content = QWidget()
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(15)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        project_info_group = QGroupBox("Project Information")
        project_info_layout = QVBoxLayout()
        project_info_layout.setSpacing(5)
        
        project_row1 = QHBoxLayout()
        project_row1.addWidget(QLabel("Project:"))
        self.simple_project_label = QLabel(self.project.name)
        project_row1.addWidget(self.simple_project_label)
        project_row1.addStretch()
        project_info_layout.addLayout(project_row1)
        
        project_row2 = QHBoxLayout()
        project_row2.addWidget(QLabel("Author:"))
        self.simple_author_label = QLabel(self.project.author)
        project_row2.addWidget(self.simple_author_label)
        project_row2.addStretch()
        project_info_layout.addLayout(project_row2)
        
        project_row3 = QHBoxLayout()
        project_row3.addWidget(QLabel("Version:"))
        self.simple_version_label = QLabel("Not selected")
        project_row3.addWidget(self.simple_version_label)
        project_row3.addStretch()
        project_info_layout.addLayout(project_row3)
        
        project_row4 = QHBoxLayout()
        project_row4.addWidget(QLabel("GitHub:"))
        self.simple_github_label = QLabel(self.project.github_url if self.project.github_url else "Not set")
        if self.project.github_url:
            self.simple_github_label.setText(f'<a href="{self.project.github_url}"  style="color: #2a82da; text-decoration: none;">{self.project.github_url}</a>')
            self.simple_github_label.setOpenExternalLinks(True)
        project_row4.addWidget(self.simple_github_label)
        project_row4.addStretch()
        project_info_layout.addLayout(project_row4)
        
        project_info_group.setLayout(project_info_layout)
        stats_layout.addWidget(project_info_group)
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        stats_layout.addWidget(line2)
        
        tasks_stats_group = QGroupBox("Tasks")
        tasks_stats_layout = QVBoxLayout()
        tasks_stats_layout.setSpacing(5)
        
        tasks_row1 = QHBoxLayout()
        tasks_row1.addWidget(QLabel("Total:"))
        self.simple_total_tasks = QLabel("0")
        tasks_row1.addWidget(self.simple_total_tasks)
        tasks_row1.addSpacing(20)
        tasks_row1.addWidget(QLabel("Todo:"))
        self.simple_todo_tasks = QLabel("0")
        tasks_row1.addWidget(self.simple_todo_tasks)
        tasks_row1.addSpacing(20)
        tasks_row1.addWidget(QLabel("In Progress:"))
        self.simple_inprogress_tasks = QLabel("0")
        tasks_row1.addWidget(self.simple_inprogress_tasks)
        tasks_row1.addSpacing(20)
        tasks_row1.addWidget(QLabel("Done:"))
        self.simple_done_tasks = QLabel("0")
        tasks_row1.addWidget(self.simple_done_tasks)
        tasks_row1.addStretch()
        tasks_stats_layout.addLayout(tasks_row1)
        
        priority_label = QLabel("By Priority:")
        priority_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        tasks_stats_layout.addWidget(priority_label)
        
        priority_row = QHBoxLayout()
        priority_row.addWidget(QLabel("Critical:"))
        self.simple_critical_tasks = QLabel("0")
        priority_row.addWidget(self.simple_critical_tasks)
        priority_row.addSpacing(20)
        priority_row.addWidget(QLabel("High:"))
        self.simple_high_tasks = QLabel("0")
        priority_row.addWidget(self.simple_high_tasks)
        priority_row.addSpacing(20)
        priority_row.addWidget(QLabel("Medium:"))
        self.simple_medium_tasks = QLabel("0")
        priority_row.addWidget(self.simple_medium_tasks)
        priority_row.addSpacing(20)
        priority_row.addWidget(QLabel("Low:"))
        self.simple_low_tasks = QLabel("0")
        priority_row.addWidget(self.simple_low_tasks)
        priority_row.addStretch()
        tasks_stats_layout.addLayout(priority_row)
        
        tasks_stats_group.setLayout(tasks_stats_layout)
        stats_layout.addWidget(tasks_stats_group)
        
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setFrameShadow(QFrame.Sunken)
        stats_layout.addWidget(line3)
        
        bugs_stats_group = QGroupBox("Bugs")
        bugs_stats_layout = QVBoxLayout()
        bugs_stats_layout.setSpacing(5)
        
        bugs_row1 = QHBoxLayout()
        bugs_row1.addWidget(QLabel("Total:"))
        self.simple_total_bugs = QLabel("0")
        bugs_row1.addWidget(self.simple_total_bugs)
        bugs_row1.addSpacing(20)
        bugs_row1.addWidget(QLabel("Open:"))
        self.simple_open_bugs = QLabel("0")
        bugs_row1.addWidget(self.simple_open_bugs)
        bugs_row1.addSpacing(20)
        bugs_row1.addWidget(QLabel("In Progress:"))
        self.simple_inprogress_bugs = QLabel("0")
        bugs_row1.addWidget(self.simple_inprogress_bugs)
        bugs_row1.addSpacing(20)
        bugs_row1.addWidget(QLabel("Fixed:"))
        self.simple_fixed_bugs = QLabel("0")
        bugs_row1.addWidget(self.simple_fixed_bugs)
        bugs_row1.addStretch()
        bugs_stats_layout.addLayout(bugs_row1)
        
        bug_priority_label = QLabel("By Priority:")
        bug_priority_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        bugs_stats_layout.addWidget(bug_priority_label)
        
        bug_priority_row = QHBoxLayout()
        bug_priority_row.addWidget(QLabel("Critical:"))
        self.simple_critical_bugs = QLabel("0")
        bug_priority_row.addWidget(self.simple_critical_bugs)
        bug_priority_row.addSpacing(20)
        bug_priority_row.addWidget(QLabel("High:"))
        self.simple_high_bugs = QLabel("0")
        bug_priority_row.addWidget(self.simple_high_bugs)
        bug_priority_row.addSpacing(20)
        bug_priority_row.addWidget(QLabel("Medium:"))
        self.simple_medium_bugs = QLabel("0")
        bug_priority_row.addWidget(self.simple_medium_bugs)
        bug_priority_row.addSpacing(20)
        bug_priority_row.addWidget(QLabel("Low:"))
        self.simple_low_bugs = QLabel("0")
        bug_priority_row.addWidget(self.simple_low_bugs)
        bug_priority_row.addStretch()
        bugs_stats_layout.addLayout(bug_priority_row)
        
        bugs_stats_group.setLayout(bugs_stats_layout)
        stats_layout.addWidget(bugs_stats_group)
        
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setFrameShadow(QFrame.Sunken)
        stats_layout.addWidget(line4)
        
        export_layout = QHBoxLayout()
        export_layout.setSpacing(10)
        
        export_stats_btn = QPushButton("Export Statistics")
        export_stats_btn.clicked.connect(self._export_statistics)
        export_stats_btn.setMinimumHeight(40)
        export_layout.addWidget(export_stats_btn)
        
        export_report_btn = QPushButton("Export Full Report")
        export_report_btn.clicked.connect(self._export_full_report)
        export_report_btn.setMinimumHeight(40)
        export_layout.addWidget(export_report_btn)
        
        stats_layout.addLayout(export_layout)
        stats_layout.addStretch()
        
        stats_content.setLayout(stats_layout)
        stats_scroll.setWidget(stats_content)
        
        main_layout.addWidget(stats_scroll)
        
        widget.setLayout(main_layout)
        return widget
    
    def _update_statistics(self):
        if not self.task_manager or not self.bug_manager:
            self._set_simple_empty_stats()
            return
        
        stats = StatisticsGenerator.generate_project_stats(
            self.project, self.task_manager, self.bug_manager
        )
        
        progress_info = stats["progress"]
        task_percentage = progress_info["completion_rate"]
        bug_percentage = progress_info["bug_resolution_rate"]
        
        self.simple_task_progress_bar.setValue(int(task_percentage))
        self.simple_task_percent.setText(f"{task_percentage}%")
        
        self.simple_bug_progress_bar.setValue(int(bug_percentage))
        self.simple_bug_percent.setText(f"{bug_percentage}%")
                
        self.simple_version_label.setText(self.current_version if self.current_version else "Not selected")
        self.simple_project_label.setText(self.project.name)
        self.simple_author_label.setText(self.project.author)
        
        task_info = stats["tasks"]
        self.simple_total_tasks.setText(str(task_info['total']))
        self.simple_todo_tasks.setText(str(task_info['status_summary']['todo']))
        self.simple_inprogress_tasks.setText(str(task_info['status_summary']['in_progress']))
        self.simple_done_tasks.setText(str(task_info['status_summary']['done']))
        
        by_priority = task_info['by_priority']
        self.simple_critical_tasks.setText(str(by_priority['critical']))
        self.simple_high_tasks.setText(str(by_priority['high']))
        self.simple_medium_tasks.setText(str(by_priority['medium']))
        self.simple_low_tasks.setText(str(by_priority['low']))
        
        bug_info = stats["bugs"]
        self.simple_total_bugs.setText(str(bug_info['total']))
        self.simple_open_bugs.setText(str(bug_info['open']))
        self.simple_inprogress_bugs.setText(str(bug_info['by_status'].get('in_progress', 0)))
        self.simple_fixed_bugs.setText(str(bug_info['fixed']))
        
        bug_by_priority = bug_info['by_priority']
        self.simple_critical_bugs.setText(str(bug_by_priority['critical']))
        self.simple_high_bugs.setText(str(bug_by_priority['high']))
        self.simple_medium_bugs.setText(str(bug_by_priority['medium']))
        self.simple_low_bugs.setText(str(bug_by_priority['low']))

    def _set_simple_empty_stats(self):
        self.simple_task_progress_bar.setValue(0)
        self.simple_task_percent.setText("0%")
        self.simple_bug_progress_bar.setValue(0)
        self.simple_bug_percent.setText("0%")
        self.simple_ratio_label.setText("0.00")
        
        self.simple_version_label.setText("Not selected")
        self.simple_project_label.setText(self.project.name)
        self.simple_author_label.setText(self.project.author)
        
        self.simple_total_tasks.setText("0")
        self.simple_todo_tasks.setText("0")
        self.simple_inprogress_tasks.setText("0")
        self.simple_done_tasks.setText("0")
        
        self.simple_critical_tasks.setText("0")
        self.simple_high_tasks.setText("0")
        self.simple_medium_tasks.setText("0")
        self.simple_low_tasks.setText("0")
        
        self.simple_total_bugs.setText("0")
        self.simple_open_bugs.setText("0")
        self.simple_inprogress_bugs.setText("0")
        self.simple_fixed_bugs.setText("0")
        
        self.simple_critical_bugs.setText("0")
        self.simple_high_bugs.setText("0")
        self.simple_medium_bugs.setText("0")
        self.simple_low_bugs.setText("0")
    
    def _switch_to_tester_mode(self):
        from core.ui.windows.tester_window import TesterWindow
        reply = QMessageBox.question(
            self,
            "Switch Mode",
            "Switch to Tester mode? All unsaved changes will be saved.\n\n"
            "Note: Some developer-specific features will not be available.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self._save_project():
                main_window = self.parent()
                
                tester_window = TesterWindow(self.project, self.filepath, main_window)
                tester_window.show()
                
                self.hide()
            else:
                QMessageBox.warning(self, "Error", "Failed to save project. Please try again.")
    
    def _clear_selection(self):
        self.tasks_table.clearSelection()
        self.bugs_table.clearSelection()
        self.selected_task_id = None
        self.selected_bug_id = None
    
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
        
        self._clear_selection()
        
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

        for row in range(len(tasks)):
            self.tasks_table.setRowHeight(row, 40)
        
        for row, task in enumerate(tasks):
            id_item = QTableWidgetItem(task.id)
            id_item.setData(Qt.UserRole, task.id)
            
            title_item = QTableWidgetItem(task.title)

            description_item = QTableWidgetItem(task.description)
            
            priority_item = QTableWidgetItem(task.priority.value.upper())
            
            status_item = QTableWidgetItem(task.status.value.replace('_', ' ').title())
            
            bugs_count = len(self.bug_manager.get_bugs_by_task(task.id)) if self.bug_manager else 0
            bugs_item = QTableWidgetItem(str(bugs_count))
            
            status_text = task.status.value.replace('_', ' ').title()
            
            status_color = task.get_status_color()
            status_item.setForeground(status_color)
            
            if task.status == TaskStatus.DONE:
                done_color = QColor(60, 150, 60, 30)
                for item in [id_item, title_item, description_item, priority_item, status_item, bugs_item]:
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
            
            self.tasks_table.setItem(row, 0, title_item)
            self.tasks_table.setItem(row, 1, description_item)
            self.tasks_table.setItem(row, 2, priority_item)
            self.tasks_table.setItem(row, 3, status_item)
            self.tasks_table.setItem(row, 4, bugs_item)
            self.tasks_table.setItem(row, 5, id_item)
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)
            
            view_btn = QPushButton("👁️")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
            view_btn.setToolTip("View task details")
            view_btn.clicked.connect(lambda checked, t=task: self._view_task_details(t))
            
            if task.status == TaskStatus.IN_PROGRESS:
                done_btn = QPushButton("✅")
                done_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #388E3C;
                    }
                    QPushButton:pressed {
                        background-color: #1B5E20;
                    }
                """)
                done_btn.setToolTip("Mark as Done")
                done_btn.clicked.connect(lambda checked, t=task: self._mark_task_status(t, TaskStatus.DONE))
                actions_layout.addWidget(done_btn)
            else:
                in_progress_btn = QPushButton("🔄")
                in_progress_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
                in_progress_btn.setToolTip("Mark as In Progress")
                in_progress_btn.clicked.connect(lambda checked, t=task: self._mark_task_status(t, TaskStatus.IN_PROGRESS))
                actions_layout.addWidget(in_progress_btn)

            
            delete_btn = QPushButton("🗑️")
            delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #B71C1C;
                    }
                """)
            delete_btn.setToolTip("Delete task")
            delete_btn.clicked.connect(lambda checked, t=task: self._delete_task(t))
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            actions_widget.setLayout(actions_layout)
            
            self.tasks_table.setCellWidget(row, 6, actions_widget)
        
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
        
        self._clear_selection()
        
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
        task_id_item = self.tasks_table.item(row, 5)
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
        
        task_id_item = self.tasks_table.item(selected_row, 5)
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

        for row in range(len(bugs)):
            self.bugs_table.setRowHeight(row, 40)
        
        for row, bug in enumerate(bugs):
            
            title_item = QTableWidgetItem(bug.title)
            self.bugs_table.setItem(row, 0, title_item)
            
            priority_item = QTableWidgetItem(bug.priority.value.upper())
            
            if bug.priority == BugPriority.CRITICAL:
                priority_item.setForeground(QColor(255, 100, 100))
            elif bug.priority == BugPriority.HIGH:
                priority_item.setForeground(QColor(255, 150, 50))
            elif bug.priority == BugPriority.MEDIUM:
                priority_item.setForeground(QColor(255, 200, 50))
            else:
                priority_item.setForeground(QColor(150, 200, 150))
            
            self.bugs_table.setItem(row, 1, priority_item)
            
            status_item = QTableWidgetItem(bug.status.value.replace('_', ' ').title())
            status_color = bug.get_status_color()
            status_item.setForeground(QColor(status_color))
            self.bugs_table.setItem(row, 2, status_item)
            
            task_display_text = ""
            if bug.task_id and self.task_manager:
                task = self.task_manager.get_task(bug.task_id)
                if task:
                    task_display_text = f"{task.title}"
                else:
                    task_display_text = f"{bug.task_id} (not found)"
            else:
                task_display_text = "No task"
            
            task_item = QTableWidgetItem(task_display_text)
            task_item.setData(Qt.UserRole, bug.task_id if bug.task_id else "")
            self.bugs_table.setItem(row, 3, task_item)
            
            date_str = bug.created_at[:10] if bug.created_at else "N/A"
            date_item = QTableWidgetItem(date_str)
            self.bugs_table.setItem(row, 4, date_item)

            id_item = QTableWidgetItem(bug.id)
            id_item.setData(Qt.UserRole, bug.id)
            self.bugs_table.setItem(row, 5, id_item)

            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)
            
            view_btn = QPushButton("👁️")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
            view_btn.setToolTip("View bug details")
            view_btn.clicked.connect(lambda checked, b=bug: self._view_bug_details(b))
            
            if bug.status == BugStatus.IN_PROGRESS:
                done_btn = QPushButton("✅")
                done_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #388E3C;
                    }
                    QPushButton:pressed {
                        background-color: #1B5E20;
                    }
                """)
                done_btn.setToolTip("Mark as Done")
                done_btn.clicked.connect(lambda checked, b=bug: self._mark_bug_status(b, BugStatus.FIXED))
                actions_layout.addWidget(done_btn)
            else:
                in_progress_btn = QPushButton("🔄")
                in_progress_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
                in_progress_btn.setToolTip("Mark as In Progress")
                in_progress_btn.clicked.connect(lambda checked, b=bug: self._mark_bug_status(b, BugStatus.IN_PROGRESS))
                actions_layout.addWidget(in_progress_btn)
            
            actions_layout.addWidget(view_btn)
            actions_layout.addStretch()
            
            actions_widget.setLayout(actions_layout)
            
            self.bugs_table.setCellWidget(row, 6, actions_widget)

        
        self.bugs_table.sortItems(6, Qt.DescendingOrder)
    
    def _clear_bug_filters(self):
        self.bug_filter_status.setCurrentText("All Statuses")
        self.bug_filter_priority.setCurrentText("All Priorities")
        self.bug_search_input.clear()
        self._clear_selection()
        self._refresh_bugs_table()
    
    def _on_bug_double_clicked(self, item):
        row = item.row()
        bug_id_item = self.bugs_table.item(row, 5)
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
        
        bug_id_item = self.bugs_table.item(selected_row, 5)
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
        
        self._clear_selection()
        
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
        
        task_id_item = self.tasks_table.item(selected_row, 5)
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
        
        task_id_item = self.tasks_table.item(selected_row, 5)
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
        
        task_id_item = self.tasks_table.item(selected_row, 5)
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
        
        bug_id_item = self.bugs_table.item(selected_row, 5)
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
        <p><a href="https://github.com/aixandrolab/smart-bug-tracker" style="color: #2a82da; text-decoration: none;">GitHub Repository</a></p>
        """
        
        QMessageBox.about(self, "About Smart Bug Tracker", about_text)

    def _show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Keyboard Shortcuts Help")
        help_dialog.setFixedSize(800, 600)
        
        main_layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        help_text_widget = QWidget()
        text_layout = QVBoxLayout()
        
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
        <p><b>Ctrl+Shift+D:</b> Mark bug as fixed</p>
        <p><b>Ctrl+Shift+P:</b> Mark bug as in progress</p>
        
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
        
        <hr>
        
        <h3>Task Statuses</h3>
        <p><b>Todo:</b> Task not started</p>
        <p><b>In Progress:</b> Currently working on</p>
        <p><b>Ready for Test:</b> Ready for testing</p>
        <p><b>Testing:</b> Under testing</p>
        <p><b>Done:</b> Completed</p>
        <p><b>Blocked:</b> Blocked by dependencies</p>
        
        <hr>
        
        <h3>Bug Statuses</h3>
        <p><b>Open:</b> Bug reported, not addressed</p>
        <p><b>In Progress:</b> Being fixed</p>
        <p><b>Fixed:</b> Bug resolved</p>
        <p><b>Won't Fix:</b> Will not be fixed</p>
        <p><b>Duplicate:</b> Duplicate of another bug</p>
        <p><b>Invalid:</b> Not a valid bug</p>
        
        <hr>
        
        <h3>Priority Levels</h3>
        <p><b>Critical:</b> Highest priority, immediate action required</p>
        <p><b>High:</b> Important, fix soon</p>
        <p><b>Medium:</b> Normal priority</p>
        <p><b>Low:</b> Low priority, can be postponed</p>
        """
        
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setAlignment(Qt.AlignLeft)
        
        text_layout.addWidget(help_label)
        help_text_widget.setLayout(text_layout)
        scroll_area.setWidget(help_text_widget)
        
        main_layout.addWidget(scroll_area)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5a7a;
            }
        """)
        close_button.clicked.connect(help_dialog.accept)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)
        
        help_dialog.setLayout(main_layout)
        help_dialog.exec_()
