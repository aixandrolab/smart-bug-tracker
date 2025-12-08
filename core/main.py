from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QDialog, QFileDialog, QLineEdit, QTextEdit, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.project import Project
from core.project_file_handler import ProjectFileHandler

import os


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.task import Task, TaskPriority, TaskStatus
from core.task_manager import TaskManager


class RoleSelectionDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Role")
        self.setFixedSize(400, 300)
        self.selected_role = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header_label = QLabel("Select role for working with project")
        header_label.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        layout.addSpacing(30)
        
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
            
            role_dialog = RoleSelectionDialog(self)
            if role_dialog.exec_() == QDialog.Accepted:
                role = role_dialog.selected_role
                
                if role == "developer":
                    self.developer_window = DeveloperWindow(project, filepath, self)
                    self.developer_window.show()
                    self.hide()
                    
                elif role == "tester":
                    QMessageBox.information(
                        self, 
                        "Project Loaded",
                        f"Project '{project.name}' loaded as Tester\n"
                        f"Tester window coming soon!"
                    )
        else:
            QMessageBox.warning(self, "Error", "Failed to load project")
    
    def on_help(self):
        QMessageBox.information(
            self,
            'Smart Bug Tracker Help',
            '📂 <a href="https://github.com/aixandrolab/smart-bug-tracker" style="color: #2a82da;">GitHub Repository</a><br>'
        )

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DeveloperWindow(QMainWindow):
    
    def __init__(self, project, filepath, parent=None):
        super().__init__(parent)
        self.project = project
        self.filepath = filepath
        
        self.task_manager = None
        self.current_version = ""
        
        self.project_data = ProjectFileHandler.load_project_full(filepath)
        if not self.project_data:
            QMessageBox.critical(self, "Error", "Failed to load project data")
            self.close()
            return
        
        self.setWindowTitle(f"BugTracker - {project.name} [Developer]")
        self.setGeometry(100, 100, 1200, 800)
        
        self._setup_ui()
        self._setup_menu()
        
        if hasattr(self, 'tasks_table'):
            self.tasks_table.itemSelectionChanged.connect(self._on_task_selected)
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        save_action = QAction("Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_project)
        file_menu.addAction(save_action)
        
        export_action = QAction("Export JSON", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self._export_json)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        project_menu = menubar.addMenu("Project")
        
        version_action = QAction("Manage Versions", self)
        version_action.triggered.connect(self._manage_versions)
        project_menu.addAction(version_action)
        
        view_menu = menubar.addMenu("View")
        
        show_all_action = QAction("Show All Tasks", self)
        show_all_action.triggered.connect(lambda: self._filter_tasks("all"))
        view_menu.addAction(show_all_action)
        
        show_critical_action = QAction("Show Critical Only", self)
        show_critical_action.triggered.connect(lambda: self._filter_tasks("critical"))
        view_menu.addAction(show_critical_action)
        
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("Help", self)
        help_action.triggered.connect(self._show_help)
        help_menu.addAction(help_action)
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        top_panel = self._create_top_panel()
        main_layout.addLayout(top_panel)
        
        main_layout.addSpacing(10)
        
        splitter = QSplitter(Qt.Horizontal)
        
        self.tasks_widget = self._create_tasks_widget()
        splitter.addWidget(self.tasks_widget)
        
        self.details_widget = self._create_details_widget()
        splitter.addWidget(self.details_widget)
        
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        
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
        new_version_btn.clicked.connect(self._create_new_version)
        layout.addWidget(new_version_btn)
        
        layout.addStretch()
        
        new_task_btn = QPushButton("📝 Add Test Task")
        new_task_btn.clicked.connect(self._add_test_task)
        layout.addWidget(new_task_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._refresh_data)
        layout.addWidget(refresh_btn)
        
        return layout
    
    def _create_tasks_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        header = QLabel("Test Tasks")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(4)
        self.tasks_table.setHorizontalHeaderLabels(["ID", "Title", "Priority", "Bugs"])
        self.tasks_table.horizontalHeader().setStretchLastSection(True)
        self.tasks_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self._show_tasks_context_menu)
        
        layout.addWidget(self.tasks_table)
        
        widget.setLayout(layout)
        return widget
    
    def _create_details_widget(self):
        tab_widget = QTabWidget()
        
        self.task_details_widget = QWidget()
        self._setup_task_details_tab()
        tab_widget.addTab(self.task_details_widget, "Task Details")
        
        self.bugs_widget = QWidget()
        self._setup_bugs_tab()
        tab_widget.addTab(self.bugs_widget, "Bugs")
        
        self.stats_widget = QWidget()
        self._setup_stats_tab()
        tab_widget.addTab(self.stats_widget, "Statistics")
        
        return tab_widget
    
    def _setup_task_details_tab(self):
        layout = QVBoxLayout()
        
        self.task_title_label = QLabel("Select a task to view details")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.task_title_label.setFont(title_font)
        layout.addWidget(self.task_title_label)
        
        layout.addSpacing(10)
        
        self.task_desc_text = QTextEdit()
        self.task_desc_text.setMaximumHeight(100)
        layout.addWidget(QLabel("Description:"))
        self.task_desc_text = QTextEdit()
        layout.addWidget(self.task_desc_text)

        save_description_btn = QPushButton("Save Description")
        save_description_btn.clicked.connect(self._save_test_description)
        layout.addWidget(save_description_btn)
        
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("Priority:"))
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Critical", "High", "Medium", "Low"])
        priority_layout.addWidget(self.priority_combo)
        
        update_priority_btn = QPushButton("Update Priority")
        update_priority_btn.clicked.connect(self._update_task_priority)
        priority_layout.addWidget(update_priority_btn)
        
        priority_layout.addStretch()
        layout.addLayout(priority_layout)
        
        layout.addSpacing(20)
        
        layout.addWidget(QLabel("Test Instructions:"))
        self.test_instructions_text = QTextEdit()
        self.test_instructions_text.setMaximumHeight(150)
        layout.addWidget(self.test_instructions_text)
        
        save_instructions_btn = QPushButton("Save Instructions")
        save_instructions_btn.clicked.connect(self._save_test_instructions)
        layout.addWidget(save_instructions_btn)
        
        layout.addStretch()
        
        self.task_details_widget.setLayout(layout)
    
    def _setup_bugs_tab(self):
        layout = QVBoxLayout()
        
        self.bugs_table = QTableWidget()
        self.bugs_table.setColumnCount(5)
        self.bugs_table.setHorizontalHeaderLabels(["ID", "Title", "Status", "Priority", "Date"])
        self.bugs_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.bugs_table)
        
        layout.addWidget(QLabel("Bug Details:"))
        self.bug_details_text = QTextEdit()
        self.bug_details_text.setReadOnly(True)
        self.bug_details_text.setMaximumHeight(100)
        layout.addWidget(self.bug_details_text)
        
        action_layout = QHBoxLayout()
        
        mark_fixed_btn = QPushButton("Mark as Fixed")
        mark_fixed_btn.clicked.connect(self._mark_bug_fixed)
        action_layout.addWidget(mark_fixed_btn)
        
        add_comment_btn = QPushButton("Add Comment")
        add_comment_btn.clicked.connect(self._add_bug_comment)
        action_layout.addWidget(add_comment_btn)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        self.bugs_widget.setLayout(layout)
    
    def _setup_stats_tab(self):
        layout = QVBoxLayout()
        
        self.total_tasks_label = QLabel("Total Tasks: 0")
        layout.addWidget(self.total_tasks_label)
        
        self.critical_tasks_label = QLabel("Critical Tasks: 0")
        layout.addWidget(self.critical_tasks_label)
        
        self.open_bugs_label = QLabel("Open Bugs: 0")
        layout.addWidget(self.open_bugs_label)
        
        self.fixed_bugs_label = QLabel("Fixed Bugs: 0")
        layout.addWidget(self.fixed_bugs_label)
        
        layout.addStretch()
        
        export_stats_btn = QPushButton("Export Statistics to JSON")
        export_stats_btn.clicked.connect(self._export_statistics)
        layout.addWidget(export_stats_btn)
        
        self.stats_widget.setLayout(layout)
        
    def _on_version_changed(self, version):
        if version != "Select version...":
            self.current_version = version
            self._load_version_data(version)
    
    def _load_version_data(self, version):
        self.current_version = version
        
        self.task_manager = TaskManager(self.project_data, version)
        
        self.statusBar().showMessage(
            f"Version: {version} | Tasks: {self.task_manager.count} | "
            f"Todo: {self.task_manager.todo_count} | "
            f"Critical: {self.task_manager.critical_count}"
        )
        
        self._refresh_tasks_table()
        self._update_statistics()
    
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
                    self._refresh_tasks_table()
                    self._update_statistics()
                    
                    self._save_project()
                    
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"Task '{task.title}' added successfully!"
                    )
                else:
                    QMessageBox.warning(self, "Error", "Failed to add task")
    
    def _refresh_tasks_table(self):
        if not self.task_manager:
            self.tasks_table.setRowCount(0)
            return
        
        tasks = self.task_manager.get_all_tasks()
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
                priority_item.setForeground(QColor(255, 255, 100))
            else:
                priority_item.setForeground(QColor(150, 255, 150))
            
            self.tasks_table.setItem(row, 2, priority_item)
            
            bugs_item = QTableWidgetItem(str(len(task.bug_ids)))
            self.tasks_table.setItem(row, 3, bugs_item)
        
        self.tasks_table.sortItems(0, Qt.AscendingOrder)
    
    def _on_task_selected(self):
        if not self.task_manager:
            return
        
        selected_items = self.tasks_table.selectedItems()
        if not selected_items:
            return
        
        task_id_item = self.tasks_table.item(self.tasks_table.currentRow(), 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        task = self.task_manager.get_task(task_id)
        
        if task:
            self.task_title_label.setText(task.title)
            self.task_desc_text.setPlainText(task.description)
            
            priority_index = {
                TaskPriority.CRITICAL: 0,
                TaskPriority.HIGH: 1,
                TaskPriority.MEDIUM: 2,
                TaskPriority.LOW: 3
            }
            self.priority_combo.setCurrentIndex(
                priority_index.get(task.priority, 2)
            )
            
            self.test_instructions_text.setPlainText(task.test_instructions)
    
    def _show_tasks_context_menu(self, position):
        if not self.task_manager:
            return
        
        menu = QMenu()
        
        edit_action = menu.addAction("✏️ Edit Task")
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
        delete_action.triggered.connect(lambda: self._delete_task(task))
        mark_in_progress.triggered.connect(lambda: self._mark_task_status(task, TaskStatus.IN_PROGRESS))
        mark_done.triggered.connect(lambda: self._mark_task_status(task, TaskStatus.DONE))
        
        menu.exec_(self.tasks_table.viewport().mapToGlobal(position))
    
    def _edit_task(self, task):
        dialog = EditTaskDialog(task, self)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_updated_task_data()
            if updated_data and self.task_manager.update_task(task.id, **updated_data):
                self._refresh_tasks_table()
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
                self._refresh_tasks_table()
                self._update_statistics()
                self._save_project()
                QMessageBox.information(self, "Success", "Task deleted successfully!")
    
    def _mark_task_status(self, task, status):
        if self.task_manager.update_task(task.id, status=status):
            self._refresh_tasks_table()
            self._save_project()
            status_text = status.value.replace('_', ' ').title()
            self.statusBar().showMessage(f"Task marked as {status_text}", 3000)
    
    def _update_task_priority(self):
        if not self.task_manager:
            return
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a task first!")
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        
        priority_map = {
            "Critical": TaskPriority.CRITICAL,
            "High": TaskPriority.HIGH,
            "Medium": TaskPriority.MEDIUM,
            "Low": TaskPriority.LOW
        }
        
        new_priority = priority_map[self.priority_combo.currentText()]
        
        if self.task_manager.update_task(task_id, priority=new_priority):
            self._refresh_tasks_table()
            self._save_project()
            self.statusBar().showMessage("Priority updated successfully!", 3000)
    
    def _save_test_instructions(self):
        if not self.task_manager:
            return
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a task first!")
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        instructions = self.test_instructions_text.toPlainText().strip()
        
        if self.task_manager.update_task(task_id, test_instructions=instructions):
            self._save_project()
            self.statusBar().showMessage("Instructions saved successfully!", 3000)
    
    def _save_test_description(self):
        if not self.task_manager:
            return
        
        selected_row = self.tasks_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a task first!")
            return
        
        task_id_item = self.tasks_table.item(selected_row, 0)
        if not task_id_item:
            return
        
        task_id = task_id_item.data(Qt.UserRole)
        description = self.task_desc_text.toPlainText().strip()
        
        if self.task_manager.update_task(task_id, test_description=description):
            self._save_project()
            self.statusBar().showMessage("Description saved successfully!", 3000)
    
    def _update_statistics(self):
        if not self.task_manager:
            self.total_tasks_label.setText("Total Tasks: 0")
            self.critical_tasks_label.setText("Critical Tasks: 0")
            self.open_bugs_label.setText("Open Bugs: 0")
            self.fixed_bugs_label.setText("Fixed Bugs: 0")
            return
        
        stats = self.task_manager.get_task_statistics()
        self.total_tasks_label.setText(f"Total Tasks: {stats['total']}")
        self.critical_tasks_label.setText(f"Critical Tasks: {stats['critical']}")
        self.open_bugs_label.setText("Open Bugs: 0 (not implemented)")
        self.fixed_bugs_label.setText("Fixed Bugs: 0 (not implemented)")
    
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
            self._refresh_tasks_table()
            self._update_statistics()
            self.statusBar().showMessage("Data refreshed successfully!", 3000)
    
    def _filter_tasks(self, filter_type):
        QMessageBox.information(self, "Info", f"Filtering by {filter_type} - coming soon!")
    
    def _mark_bug_fixed(self):
        QMessageBox.information(self, "Info", "Bug fixing - coming soon!")
    
    def _add_bug_comment(self):
        QMessageBox.information(self, "Info", "Bug comments - coming soon!")
    
    def _export_json(self):
        QMessageBox.information(self, "Info", "Export JSON - coming soon!")
    
    def _export_statistics(self):
        QMessageBox.information(self, "Info", "Export statistics - coming soon!")
    
    def _manage_versions(self):
        QMessageBox.information(self, "Info", "Version management - coming soon!")
    
    def _show_help(self):
        QMessageBox.information(
            self,
            "Help - Developer Mode",
            "Developer can:\n"
            "1. Add test tasks\n"
            "2. View all bugs\n"
            "3. Set task priorities\n"
            "4. Manage project versions\n"
            "5. Export JSON files"
        )


class AddTaskDialog(QDialog):    
    def __init__(self, version: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Test Task - {version}")
        self.setFixedSize(500, 400)
        
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