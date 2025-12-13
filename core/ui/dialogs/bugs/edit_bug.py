from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QWidget,
    QFileDialog,
    QScrollArea
)

from typing import List

from core.models.bug import Bug, BugPriority, BugStatus
from core.models.task import Task


class EditBugDialog(QDialog):    
    def __init__(self, bug: Bug, available_tasks: List[Task], is_tester: bool = True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Bug - {bug.id}")
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