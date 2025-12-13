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
from PyQt5.QtCore import pyqtSignal

from typing import List

from core.models.bug import BugPriority
from core.models.task import Task


class AddBugDialog(QDialog):
    bug_added = pyqtSignal()
    def __init__(self, version: str, available_tasks: List[Task], parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Bug - {version}")
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
