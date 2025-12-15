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
from PyQt5.QtMultimedia import QSound

from core.models.task import TaskPriority


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

        self.click_sound = QSound('core/data/sounds/click.wav')
        self.error_sound = QSound('core/data/sounds/error.wav')
        
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
        self.add_btn.clicked.connect(self.on_click)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.on_click)
        
        self.add_btn.clicked.connect(self._add_task)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _add_task(self):
        title = self.title_input.text().strip()
        
        if not title:
            self.on_error()
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
    
    def on_click(self):
        self.click_sound.play()
    
    def on_notify(self):
        self.notify_sound.play()
    
    def on_error(self):
        self.error_sound.play()
