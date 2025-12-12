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
    QInputDialog,
    QTableWidgetItem,
    QMenu,
    QDialog,
    QFileDialog,
    QApplication,
    QApplication,
    QScrollArea,
    QGridLayout,
    QProgressBar,
    QGroupBox,
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QKeySequence, QColor

from core.managers.bug_manager import BugManager
from core.managers.task_manager import TaskManager
from core.models.bug import BugPriority, BugStatus
from core.models.task import TaskPriority, TaskStatus
from core.ui.windows.bug_detailed_window import BugDetailWindow
from core.ui.windows.task_detail_window import TaskDetailWindow
from core.ui.dialogs.bugs.add_bug import AddBugDialog
from core.ui.dialogs.bugs.edit_bug import EditBugDialog
from core.utils.project_file_handler import ProjectFileHandler
from core.utils.statistics_generator import StatisticsGenerator


class TesterWindow(QMainWindow):
    
    def __init__(self, project, filepath, parent=None):
        super().__init__(parent)
        self.project = project
        self.filepath = filepath
        
        self.task_manager = None
        self.bug_manager = None
        self.current_version = ""
        self.showMaximized() 

        self.selected_task_id = None
        self.selected_bug_id = None
        
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
        
        export_action = QAction("Export JSON", self)
        export_action.triggered.connect(self._export_json)
        file_menu.addAction(export_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        file_menu.addSeparator()

        project_menu = menubar.addMenu("Project")

        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self._save_project)
        project_menu.addAction(save_action)
        
        github_action = QAction("🌐 Open GitHub Repository", self)
        github_action.triggered.connect(self._open_github)
        project_menu.addAction(github_action)
        
        copy_url_action = QAction("📋 Copy GitHub URL", self)
        copy_url_action.triggered.connect(self._copy_github_url)
        project_menu.addAction(copy_url_action)
        
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
                padding: 0px 16px;
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
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels([ 
            "Title",
            "Description",
            "Priority", 
            "Status", 
            "Bugs", 
            "ID",
            "Actions"
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
        
        filter_panel.addWidget(new_bug_btn)
        main_layout.addLayout(filter_panel)

        self.bugs_table = QTableWidget()
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
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2b2b2b;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #2b2b2b;
            }
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #2b2b2b;")
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        project_group = QGroupBox("📁 Project Information")
        project_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #3498db;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        project_layout = QGridLayout()
        project_layout.setHorizontalSpacing(15)
        project_layout.setVerticalSpacing(8)
        
        project_layout.setColumnStretch(0, 0)
        project_layout.setColumnStretch(1, 1)
        project_layout.setColumnStretch(2, 0)
        project_layout.setColumnStretch(3, 1)
        
        project_layout.addWidget(QLabel("<b style='color: #ecf0f1;'>Project:</b>"), 0, 0)
        self.tester_project_label = QLabel(self.project.name)
        self.tester_project_label.setStyleSheet("font-size: 14px; color: #ecf0f1; padding-left: 5px;")
        project_layout.addWidget(self.tester_project_label, 0, 1)
        
        project_layout.addWidget(QLabel("<b style='color: #ecf0f1;'>Version:</b>"), 0, 2)
        self.tester_version_label = QLabel("Not selected")
        self.tester_version_label.setStyleSheet("color: #bdc3c7; padding-left: 5px;")
        project_layout.addWidget(self.tester_version_label, 0, 3)
        
        project_layout.addWidget(QLabel("<b style='color: #ecf0f1;'>GitHub:</b>"), 1, 0)
        github_text = self.project.github_url if self.project.github_url else "Not set"
        self.tester_github_label = QLabel(github_text)
        self.tester_github_label.setOpenExternalLinks(True)
        if self.project.github_url:
            self.tester_github_label.setText(f'<a href="{self.project.github_url}" style="color: #3498db; text-decoration: none;">{github_text}</a>')
            self.tester_github_label.setStyleSheet("padding-left: 5px;")
        else:
            self.tester_github_label.setStyleSheet("color: #bdc3c7; padding-left: 5px;")
        project_layout.addWidget(self.tester_github_label, 1, 1, 1, 3)
        
        project_group.setLayout(project_layout)
        content_layout.addWidget(project_group)
        
        main_stats_group = QGroupBox("📊 Testing Statistics")
        main_stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #9b59b6;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        main_stats_layout = QGridLayout()
        main_stats_layout.setSpacing(15)
        
        bug_stats_group = QGroupBox("🐛 Bug Overview")
        bug_stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #e74c3c;
                border: 1px solid #e74c3c;
                border-radius: 6px;
                padding-top: 10px;
            }
        """)
        
        bug_stats_layout = QGridLayout()
        
        self.tester_total_bugs = self._create_tester_stat_label("Total Bugs", "0", "#e74c3c")
        self.tester_open_bugs = self._create_tester_stat_label("Open", "0", "#ff6b6b")
        self.tester_fixed_bugs = self._create_tester_stat_label("Fixed", "0", "#27ae60")
        self.tester_critical_bugs = self._create_tester_stat_label("Critical", "0", "#c0392b")
        
        bug_stats_layout.addWidget(self.tester_total_bugs, 0, 0)
        bug_stats_layout.addWidget(self.tester_open_bugs, 0, 1)
        bug_stats_layout.addWidget(self.tester_fixed_bugs, 0, 2)
        bug_stats_layout.addWidget(self.tester_critical_bugs, 0, 3)
        
        bug_stats_group.setLayout(bug_stats_layout)
        main_stats_layout.addWidget(bug_stats_group, 0, 0, 1, 2)
        
        task_stats_group = QGroupBox("📋 Task Overview")
        task_stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #3498db;
                border: 1px solid #3498db;
                border-radius: 6px;
                padding-top: 10px;
            }
        """)
        
        task_stats_layout = QGridLayout()
        
        self.tester_total_tasks = self._create_tester_stat_label("Total Tasks", "0", "#3498db")
        self.tester_todo_tasks = self._create_tester_stat_label("To Do", "0", "#f39c12")
        self.tester_in_progress_tasks = self._create_tester_stat_label("In Progress", "0", "#2980b9")
        self.tester_done_tasks = self._create_tester_stat_label("Done", "0", "#27ae60")
        
        task_stats_layout.addWidget(self.tester_total_tasks, 0, 0)
        task_stats_layout.addWidget(self.tester_todo_tasks, 0, 1)
        task_stats_layout.addWidget(self.tester_in_progress_tasks, 0, 2)
        task_stats_layout.addWidget(self.tester_done_tasks, 0, 3)
        
        task_stats_group.setLayout(task_stats_layout)
        main_stats_layout.addWidget(task_stats_group, 1, 0, 1, 2)
        
        progress_group = QGroupBox("📈 Progress")
        progress_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #ecf0f1;
                border: 1px solid #4a6278;
                border-radius: 6px;
                padding-top: 10px;
            }
        """)
        
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(10)
        
        self.tester_bug_progress_bar = QProgressBar()
        self.tester_bug_progress_bar.setRange(0, 100)
        self.tester_bug_progress_bar.setValue(0)
        self.tester_bug_progress_bar.setFormat("Bug Resolution: %p%")
        self.tester_bug_progress_bar.setStyleSheet("""
            QProgressBar {
                height: 25px;
                border: 1px solid #4a6278;
                border-radius: 5px;
                text-align: center;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #e74c3c;
                border-radius: 4px;
            }
        """)
        
        self.tester_task_progress_bar = QProgressBar()
        self.tester_task_progress_bar.setRange(0, 100)
        self.tester_task_progress_bar.setValue(0)
        self.tester_task_progress_bar.setFormat("Task Completion: %p%")
        self.tester_task_progress_bar.setStyleSheet("""
            QProgressBar {
                height: 25px;
                border: 1px solid #4a6278;
                border-radius: 5px;
                text-align: center;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                border-radius: 4px;
            }
        """)
        
        progress_layout.addWidget(self.tester_bug_progress_bar)
        progress_layout.addWidget(self.tester_task_progress_bar)
        progress_group.setLayout(progress_layout)
        main_stats_layout.addWidget(progress_group, 2, 0, 1, 2)
        
        main_stats_group.setLayout(main_stats_layout)
        content_layout.addWidget(main_stats_group)
        
        priority_group = QGroupBox("🎯 Priority Distribution")
        priority_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #f39c12;
                border: 2px solid #f39c12;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        priority_layout = QHBoxLayout()
        priority_layout.setSpacing(15)
        
        self.tester_bug_priority_chart = QLabel("Bug priorities will appear here")
        self.tester_bug_priority_chart.setAlignment(Qt.AlignCenter)
        self.tester_bug_priority_chart.setStyleSheet("""
            QLabel {
                border: 1px solid #4a6278;
                border-radius: 6px;
                padding: 15px;
                min-width: 200px;
                min-height: 150px;
                color: #ecf0f1;
                font-family: 'Consolas', 'Monospace';
                font-size: 12px;
            }
        """)
        
        self.tester_task_priority_chart = QLabel("Task priorities will appear here")
        self.tester_task_priority_chart.setAlignment(Qt.AlignCenter)
        self.tester_task_priority_chart.setStyleSheet("""
            QLabel {
                border: 1px solid #4a6278;
                border-radius: 6px;
                padding: 15px;
                min-width: 200px;
                min-height: 150px;
                color: #ecf0f1;
                font-family: 'Consolas', 'Monospace';
                font-size: 12px;
            }
        """)
        
        priority_layout.addWidget(self.tester_bug_priority_chart)
        priority_layout.addWidget(self.tester_task_priority_chart)
        priority_group.setLayout(priority_layout)
        content_layout.addWidget(priority_group)
        
        content_layout.addStretch()
        
        export_btn = QPushButton("📊 Export Testing Report")
        export_btn.clicked.connect(self._export_statistics)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #703688;
            }
        """)
        content_layout.addWidget(export_btn)
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        main_layout.addWidget(scroll)
        widget.setLayout(main_layout)
        return widget

    def _create_tester_stat_label(self, title, value, color):
        label = QLabel(f"<div style='text-align: center;'><b style='color: {color}; font-size: 18px;'>{value}</b><br><span style='color: #ecf0f1; font-size: 12px;'>{title}</span></div>")
        label.setStyleSheet(f"""
            QLabel {{
                padding: 12px;
                border: 1px solid {color};
                border-radius: 6px;
                background-color: #2c3e50;
                min-width: 80px;
            }}
        """)
        return label
        
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
        task_id_item = self.tasks_table.item(row, 5)
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

        for row in range(len(tasks)):
            self.tasks_table.setRowHeight(row, 40)
        
        for row, task in enumerate(tasks):
            
            title_item = QTableWidgetItem(task.title)
            self.tasks_table.setItem(row, 0, title_item)

            description_item = QTableWidgetItem(task.description)
            self.tasks_table.setItem(row, 1, description_item)
            
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

            id_item = QTableWidgetItem(task.id)
            id_item.setData(Qt.UserRole, task.id)
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
            
            actions_layout.addWidget(view_btn)
            actions_layout.addStretch()
            
            actions_widget.setLayout(actions_layout)
            
            self.tasks_table.setCellWidget(row, 6, actions_widget)
        
        self.tasks_table.sortItems(5, Qt.DescendingOrder)
    
    def _clear_task_filters(self):
        self.task_filter_status.setCurrentText("All Statuses")
        self.task_filter_priority.setCurrentText("All Priorities")
        self.task_search_input.clear()

        self._clear_selection()

        self._refresh_tasks_table()

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
        
    def _show_tasks_context_menu(self, position):
        if not self.task_manager:
            return
        
        menu = QMenu()
        
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
            delete_btn.clicked.connect(lambda checked, b=bug: self._delete_bug(b))
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            actions_widget.setLayout(actions_layout)
            
            self.bugs_table.setCellWidget(row, 6, actions_widget)

        
        self.bugs_table.sortItems(6, Qt.DescendingOrder)
        
        self.bugs_table.sortItems(5, Qt.DescendingOrder)

    def _clear_selection(self):
        self.tasks_table.clearSelection()
        self.bugs_table.clearSelection()
        self.selected_task_id = None
        self.selected_bug_id = None
    
    def _clear_bug_filters(self):
        self.bug_filter_status.setCurrentText("All Statuses")
        self.bug_filter_priority.setCurrentText("All Priorities")
        self.bug_search_input.clear()
        self._clear_selection()
        self._refresh_bugs_table()
    
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
            self._set_tester_empty_stats()
            return
        
        self.tester_version_label.setText(self.current_version if self.current_version else "Not selected")
        
        stats = StatisticsGenerator.generate_project_stats(
            self.project, self.task_manager, self.bug_manager
        )
        
        task_info = stats["tasks"]
        bug_info = stats["bugs"]
        progress_info = stats["progress"]
        
        self.tester_total_bugs.setText(f"<div style='text-align: center;'><b style='color: #F44336; font-size: 16px;'>{bug_info['total']}</b><br>Total Bugs</div>")
        self.tester_open_bugs.setText(f"<div style='text-align: center;'><b style='color: #FF5722; font-size: 16px;'>{bug_info['open']}</b><br>Open</div>")
        self.tester_fixed_bugs.setText(f"<div style='text-align: center;'><b style='color: #4CAF50; font-size: 16px;'>{bug_info['fixed']}</b><br>Fixed</div>")
        self.tester_critical_bugs.setText(f"<div style='text-align: center;'><b style='color: #D32F2F; font-size: 16px;'>{bug_info['by_priority']['critical']}</b><br>Critical</div>")
        
        self.tester_total_tasks.setText(f"<div style='text-align: center;'><b style='color: #2196F3; font-size: 16px;'>{task_info['total']}</b><br>Total Tasks</div>")
        self.tester_todo_tasks.setText(f"<div style='text-align: center;'><b style='color: #FF9800; font-size: 16px;'>{task_info['status_summary']['todo']}</b><br>To Do</div>")
        self.tester_in_progress_tasks.setText(f"<div style='text-align: center;'><b style='color: #03A9F4; font-size: 16px;'>{task_info['status_summary']['in_progress']}</b><br>In Progress</div>")
        self.tester_done_tasks.setText(f"<div style='text-align: center;'><b style='color: #4CAF50; font-size: 16px;'>{task_info['status_summary']['done']}</b><br>Done</div>")
        
        self.tester_bug_progress_bar.setValue(int(progress_info["bug_resolution_rate"]))
        self.tester_task_progress_bar.setValue(int(progress_info["completion_rate"]))
        
        self._update_tester_priority_charts(task_info['by_priority'], bug_info['by_priority'])

    def _update_tester_priority_charts(self, task_priorities, bug_priorities):
        bug_chart = "<b>Bug Priorities:</b><br>"
        colors = {
            "critical": "#D32F2F",
            "high": "#FF5722",
            "medium": "#FF9800",
            "low": "#4CAF50"
        }
        
        for priority, count in bug_priorities.items():
            if count > 0:
                bar = "█" * min(count, 8)
                bug_chart += f"<span style='color: {colors[priority]}'>{priority.title()}: {bar} ({count})</span><br>"
        
        self.tester_bug_priority_chart.setText(bug_chart)
        
        task_chart = "<b>Task Priorities:</b><br>"
        for priority, count in task_priorities.items():
            if count > 0:
                bar = "█" * min(count, 8)
                task_chart += f"<span style='color: {colors[priority]}'>{priority.title()}: {bar} ({count})</span><br>"
        
        self.tester_task_priority_chart.setText(task_chart)

    def _set_tester_empty_stats(self):
        self.tester_version_label.setText("Not selected")
        
        self.tester_total_bugs.setText("<div style='text-align: center;'><b style='color: #F44336; font-size: 16px;'>0</b><br>Total Bugs</div>")
        self.tester_open_bugs.setText("<div style='text-align: center;'><b style='color: #FF5722; font-size: 16px;'>0</b><br>Open</div>")
        self.tester_fixed_bugs.setText("<div style='text-align: center;'><b style='color: #4CAF50; font-size: 16px;'>0</b><br>Fixed</div>")
        self.tester_critical_bugs.setText("<div style='text-align: center;'><b style='color: #D32F2F; font-size: 16px;'>0</b><br>Critical</div>")
        
        self.tester_total_tasks.setText("<div style='text-align: center;'><b style='color: #2196F3; font-size: 16px;'>0</b><br>Total Tasks</div>")
        self.tester_todo_tasks.setText("<div style='text-align: center;'><b style='color: #FF9800; font-size: 16px;'>0</b><br>To Do</div>")
        self.tester_in_progress_tasks.setText("<div style='text-align: center;'><b style='color: #03A9F4; font-size: 16px;'>0</b><br>In Progress</div>")
        self.tester_done_tasks.setText("<div style='text-align: center;'><b style='color: #4CAF50; font-size: 16px;'>0</b><br>Done</div>")
        
        self.tester_bug_progress_bar.setValue(0)
        self.tester_task_progress_bar.setValue(0)
        
        self.tester_bug_priority_chart.setText("<b>Bug Priorities:</b><br>No data")
        self.tester_task_priority_chart.setText("<b>Task Priorities:</b><br>No data")
    
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
        
        bug_id_item = self.bugs_table.item(selected_row, 5)
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
        
        bug_id_item = self.bugs_table.item(selected_row, 5)
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
