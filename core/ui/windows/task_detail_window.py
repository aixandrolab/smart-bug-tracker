from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.models.bug import BugStatus
from core.models.task import Task, TaskPriority


class TaskDetailWindow(QDialog):
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle(f"Task Details - {task.id}")
        self.setFixedSize(600, 700)
        
        self._setup_ui()
        self._load_task_data()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        self.title_label = QLabel(self.task.title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        id_label = QLabel(f"ID: {self.task.id}")
        id_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-weight: bold;
                background-color: #2a2a2a;
                padding: 3px 10px;
                border-radius: 10px;
            }
        """)
        header_layout.addWidget(id_label)
        
        layout.addLayout(header_layout)
        
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
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        status_layout = QHBoxLayout()
        
        status_group = QGroupBox("Status")
        status_group_layout = QVBoxLayout()
        self.status_label = QLabel()
        status_font = QFont()
        status_font.setPointSize(11)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        status_group_layout.addWidget(self.status_label)
        status_group.setLayout(status_group_layout)
        status_layout.addWidget(status_group)
        
        priority_group = QGroupBox("Priority")
        priority_group_layout = QVBoxLayout()
        self.priority_label = QLabel()
        priority_font = QFont()
        priority_font.setPointSize(11)
        priority_font.setBold(True)
        self.priority_label.setFont(priority_font)
        priority_group_layout.addWidget(self.priority_label)
        priority_group.setLayout(priority_group_layout)
        status_layout.addWidget(priority_group)
        
        created_group = QGroupBox("Created")
        created_group_layout = QVBoxLayout()
        self.created_label = QLabel()
        created_group_layout.addWidget(self.created_label)
        created_group.setLayout(created_group_layout)
        status_layout.addWidget(created_group)
        
        content_layout.addLayout(status_layout)
        
        desc_group = QGroupBox("Description")
        desc_group_layout = QVBoxLayout()
        self.desc_text = QTextEdit()
        self.desc_text.setReadOnly(True)
        self.desc_text.setMaximumHeight(120)
        desc_group_layout.addWidget(self.desc_text)
        desc_group.setLayout(desc_group_layout)
        content_layout.addWidget(desc_group)
        
        instructions_group = QGroupBox("Test Instructions")
        instructions_group_layout = QVBoxLayout()
        self.instructions_text = QTextEdit()
        self.instructions_text.setReadOnly(True)
        self.instructions_text.setMaximumHeight(150)
        instructions_group_layout.addWidget(self.instructions_text)
        instructions_group.setLayout(instructions_group_layout)
        content_layout.addWidget(instructions_group)
        
        assignment_group = QGroupBox("Assignment")
        assignment_group_layout = QVBoxLayout()
        
        assigned_layout = QHBoxLayout()
        assigned_layout.addWidget(QLabel("Assigned to:"))
        self.assigned_label = QLabel()
        self.assigned_label.setStyleSheet("font-weight: bold;")
        assigned_layout.addWidget(self.assigned_label)
        assigned_layout.addStretch()
        assignment_group_layout.addLayout(assigned_layout)
        
        assignment_group.setLayout(assignment_group_layout)
        content_layout.addWidget(assignment_group)
        
        bugs_group = QGroupBox("Related Bugs")
        bugs_group_layout = QVBoxLayout()
        self.bugs_list = QListWidget()
        bugs_group_layout.addWidget(self.bugs_list)
        bugs_group.setLayout(bugs_group_layout)
        content_layout.addWidget(bugs_group)
        
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Version:"))
        self.version_label = QLabel()
        self.version_label.setStyleSheet("color: #4a9eff; font-weight: bold;")
        version_layout.addWidget(self.version_label)
        version_layout.addStretch()
        content_layout.addLayout(version_layout)
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_task_data(self):
        status_text = self.task.status.value.replace('_', ' ').title()
        status_color = self.task.get_status_color()
        self.status_label.setText(f"<span style='color: rgb({status_color.red()}, {status_color.green()}, {status_color.blue()});'>{status_text}</span>")
        
        priority_text = self.task.priority.value.upper()
        priority_color = "#FF4444" if self.task.priority == TaskPriority.CRITICAL else \
                        "#FF8800" if self.task.priority == TaskPriority.HIGH else \
                        "#FFCC00" if self.task.priority == TaskPriority.MEDIUM else "#44FF44"
        self.priority_label.setText(f"<span style='color: {priority_color};'>{priority_text}</span>")
        
        if self.task.created_at:
            created_date = self.task.created_at[:19].replace('T', ' ')
            self.created_label.setText(created_date)
        else:
            self.created_label.setText("N/A")
        
        self.desc_text.setPlainText(self.task.description)
        self.instructions_text.setPlainText(self.task.test_instructions)
        
        assigned = self.task.assigned_to if self.task.assigned_to else "Unassigned"
        self.assigned_label.setText(assigned)
        
        self.version_label.setText(self.task.version)
        
        self._load_related_bugs()
    
    def _load_related_bugs(self):
        self.bugs_list.clear()
        
        parent = self.parent()
        if hasattr(parent, 'bug_manager') and parent.bug_manager:
            bugs = parent.bug_manager.get_bugs_by_task(self.task.id)
            
            if not bugs:
                item = QListWidgetItem("No bugs for this task")
                item.setTextAlignment(Qt.AlignCenter)
                self.bugs_list.addItem(item)
                return
            
            for bug in bugs:
                status_color = bug.get_status_color()
                item_text = f"[{bug.id}] {bug.title} - {bug.status.value.replace('_', ' ').title()}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, bug.id)
                
                if bug.status == BugStatus.FIXED:
                    item.setForeground(QColor(100, 200, 100))
                elif bug.status == BugStatus.IN_PROGRESS:
                    item.setForeground(QColor(100, 150, 255))
                elif bug.status in [BugStatus.DUPLICATE, BugStatus.INVALID, BugStatus.WONT_FIX]:
                    item.setForeground(QColor(150, 150, 150))
                else:
                    item.setForeground(QColor(255, 100, 100))
                
                self.bugs_list.addItem(item)
        else:
            item = QListWidgetItem("Bug information not available")
            item.setTextAlignment(Qt.AlignCenter)
            self.bugs_list.addItem(item)