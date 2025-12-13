from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QMessageBox
)

from core.models.task import Task, TaskPriority, TaskStatus


class EditTaskDialog(QDialog):    
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Task - {task.id}")
        self.setFixedSize(800, 600)
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
