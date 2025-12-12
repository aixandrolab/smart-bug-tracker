import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.bug import Bug, BugPriority
from core.task_manager import TaskManager


class BugDetailWindow(QDialog):
    
    def __init__(self, bug: Bug, task_manager: TaskManager = None, parent=None):
        super().__init__(parent)
        self.bug = bug
        self.task_manager = task_manager
        self.setWindowTitle(f"Bug Details - {bug.id}")
        self.setFixedSize(900, 1000)
        
        self._setup_ui()
        self._load_bug_data()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        header_layout = QVBoxLayout()
        
        title_layout = QHBoxLayout()
        title_label = QLabel(f"🐛 {self.bug.title}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #ffffff;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        id_label = QLabel(f"ID: {self.bug.id}")
        id_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-weight: bold;
                background-color: #333;
                padding: 3px 12px;
                border-radius: 12px;
            }
        """)
        title_layout.addWidget(id_label)
        header_layout.addLayout(title_layout)
        
        info_bar = QWidget()
        info_bar.setStyleSheet("""
            QWidget {
                background-color: #222;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        info_layout = QHBoxLayout()
        
        self.status_badge = QLabel()
        self.status_badge.setStyleSheet("""
            QLabel {
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        info_layout.addWidget(self.status_badge)
        
        self.priority_badge = QLabel()
        self.priority_badge.setStyleSheet("""
            QLabel {
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        info_layout.addWidget(self.priority_badge)
        
        self.task_badge = QLabel()
        self.task_badge.setStyleSheet("""
            QLabel {
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
                background-color: #2a4b8d;
                color: white;
            }
        """)
        info_layout.addWidget(self.task_badge)
        
        info_layout.addStretch()
        info_bar.setLayout(info_layout)
        header_layout.addWidget(info_bar)
        
        header_widget.setLayout(header_layout)
        layout.addWidget(header_widget)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        desc_group = QGroupBox("📝 Description")
        desc_group.setStyleSheet("""
            QGroupBox {
                color: #4a9eff;
                border: 2px solid #2a4b8d;
                font-weight: bold;
                margin-top: 5px;
            }
        """)
        desc_layout = QVBoxLayout()
        self.desc_text = QTextEdit()
        self.desc_text.setReadOnly(True)
        self.desc_text.setMinimumHeight(80)
        self.desc_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        desc_layout.addWidget(self.desc_text)
        desc_group.setLayout(desc_layout)
        content_layout.addWidget(desc_group)
        
        steps_group = QGroupBox("🔄 Steps to Reproduce")
        steps_group.setStyleSheet("""
            QGroupBox {
                color: #FF9800;
                border: 2px solid #F57C00;
                font-weight: bold;
                margin-top: 5px;
            }
        """)
        steps_layout = QVBoxLayout()
        self.steps_text = QTextEdit()
        self.steps_text.setReadOnly(True)
        self.steps_text.setMinimumHeight(60)
        self.steps_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                white-space: pre-wrap;
            }
        """)
        steps_layout.addWidget(self.steps_text)
        steps_group.setLayout(steps_layout)
        content_layout.addWidget(steps_group)
        
        results_group = QGroupBox("✅ Expected vs ❌ Actual Results")
        results_group.setStyleSheet("""
            QGroupBox {
                color: #4CAF50;
                border: 2px solid #388E3C;
                font-weight: bold;
                margin-top: 5px;
            }
        """)
        results_layout = QHBoxLayout()
        
        expected_widget = QWidget()
        expected_layout = QVBoxLayout()
        expected_layout.addWidget(QLabel("Expected Result:"))
        self.expected_text = QTextEdit()
        self.expected_text.setReadOnly(True)
        self.expected_text.setMinimumHeight(60)
        self.expected_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #a0e0a0;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        expected_layout.addWidget(self.expected_text)
        expected_widget.setLayout(expected_layout)
        results_layout.addWidget(expected_widget)
        
        actual_widget = QWidget()
        actual_layout = QVBoxLayout()
        actual_layout.addWidget(QLabel("Actual Result:"))
        self.actual_text = QTextEdit()
        self.actual_text.setReadOnly(True)
        self.actual_text.setMinimumHeight(60)
        self.actual_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffa0a0;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        actual_layout.addWidget(self.actual_text)
        actual_widget.setLayout(actual_layout)
        results_layout.addWidget(actual_widget)
        
        results_group.setLayout(results_layout)
        content_layout.addWidget(results_group)
        
        meta_group = QGroupBox("📊 Metadata")
        meta_group.setStyleSheet("""
            QGroupBox {
                color: #9C27B0;
                border: 2px solid #7B1FA2;
                font-weight: bold;
                margin-top: 5px;
            }
        """)
        meta_layout = QGridLayout()
        
        meta_layout.addWidget(QLabel("Task:"), 0, 0)
        self.task_label = QLabel()
        meta_layout.addWidget(self.task_label, 0, 1)
        
        meta_layout.addWidget(QLabel("Author:"), 1, 0)
        self.author_label = QLabel()
        meta_layout.addWidget(self.author_label, 1, 1)
        
        meta_layout.addWidget(QLabel("Created:"), 2, 0)
        self.created_label = QLabel()
        meta_layout.addWidget(self.created_label, 2, 1)
        
        meta_layout.addWidget(QLabel("Assigned to:"), 3, 0)
        self.assigned_label = QLabel()
        meta_layout.addWidget(self.assigned_label, 3, 1)
        
        if self.bug.screenshot_path:
            meta_layout.addWidget(QLabel("Screenshot:"), 4, 0)
            self.screenshot_label = QLabel()
            self.screenshot_label.setOpenExternalLinks(True)
            meta_layout.addWidget(self.screenshot_label, 4, 1)
        
        meta_group.setLayout(meta_layout)
        content_layout.addWidget(meta_group)
        
        comments_group = QGroupBox("💬 Comments")
        comments_group.setStyleSheet("""
            QGroupBox {
                color: #00BCD4;
                border: 2px solid #0097A7;
                font-weight: bold;
                margin-top: 5px;
            }
        """)
        comments_layout = QVBoxLayout()
        
        comments_header = QHBoxLayout()
        comments_count = len(self.bug.comments) if self.bug.comments else 0
        comments_title = QLabel(f"Comments ({comments_count})")
        comments_title.setStyleSheet("font-weight: bold; color: #00BCD4;")
        comments_header.addWidget(comments_title)
        comments_header.addStretch()
        comments_layout.addLayout(comments_header)
        
        comments_scroll = QScrollArea()
        comments_scroll.setWidgetResizable(True)
        comments_scroll.setMinimumHeight(200)
        comments_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                border-radius: 5px;
                background-color: #1e1e1e;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        
        comments_container = QWidget()
        self.comments_container_layout = QVBoxLayout()
        self.comments_container_layout.setAlignment(Qt.AlignTop)
        self.comments_container_layout.setSpacing(5)
        self.comments_container_layout.setContentsMargins(20, 10, 20, 10)
        
        comments_container.setLayout(self.comments_container_layout)
        comments_scroll.setWidget(comments_container)
        comments_layout.addWidget(comments_scroll)
        
        comments_group.setLayout(comments_layout)
        content_layout.addWidget(comments_group)
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _load_bug_data(self):
        status_text = self.bug.status.value.replace('_', ' ').title()
        status_color = QColor(self.bug.get_status_color())
        self.status_badge.setText(status_text)
        self.status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color.name()};
                color: {'black' if status_color.lightness() > 128 else 'white'};
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
            }}
        """)
        
        priority_text = self.bug.priority.value.upper()
        priority_color = "#FF4444" if self.bug.priority == BugPriority.CRITICAL else \
                        "#FF8800" if self.bug.priority == BugPriority.HIGH else \
                        "#FFCC00" if self.bug.priority == BugPriority.MEDIUM else "#44FF44"
        self.priority_badge.setText(priority_text)
        self.priority_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {priority_color};
                color: black;
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
            }}
        """)
        
        if self.bug.task_id:
            if self.task_manager:
                task = self.task_manager.get_task(self.bug.task_id)
                if task:
                    self.task_badge.setText(f"Task: {task.title}")
                else:
                    self.task_badge.setText(f"Task: {self.bug.task_id}")
            else:
                self.task_badge.setText(f"Task: {self.bug.task_id}")
        else:
            self.task_badge.setText("No Task")
            self.task_badge.setStyleSheet("""
                QLabel {
                    padding: 3px 10px;
                    border-radius: 10px;
                    font-weight: bold;
                    background-color: #666;
                    color: white;
                }
            """)
        
        self.desc_text.setPlainText(self.bug.description)
        self.steps_text.setPlainText(self.bug.steps_to_reproduce)
        self.expected_text.setPlainText(self.bug.expected_result)
        self.actual_text.setPlainText(self.bug.actual_result)
        
        if self.bug.task_id:
            if self.task_manager:
                task = self.task_manager.get_task(self.bug.task_id)
                if task:
                    self.task_label.setText(f"{task.id}: {task.title}")
                else:
                    self.task_label.setText(self.bug.task_id)
            else:
                self.task_label.setText(self.bug.task_id)
        else:
            self.task_label.setText("No task assigned")
        
        self.author_label.setText(self.bug.author if self.bug.author else "Unknown")
        
        if self.bug.created_at:
            created_date = self.bug.created_at[:19].replace('T', ' ')
            self.created_label.setText(created_date)
        else:
            self.created_label.setText("N/A")
        
        self.assigned_label.setText(
            self.bug.assigned_to if self.bug.assigned_to else "Unassigned"
        )
        
        if hasattr(self, 'screenshot_label') and self.bug.screenshot_path:
            screenshot_path = self.bug.screenshot_path
            if os.path.exists(screenshot_path):
                self.screenshot_label.setText(
                    screenshot_path
                )
            else:
                self.screenshot_label.setText(f"File not found: {screenshot_path}")
        
        self._load_comments()
    
    def _load_comments(self):
        for i in reversed(range(self.comments_container_layout.count())): 
            widget = self.comments_container_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        if not self.bug.comments:
            no_comments_label = QLabel("No comments yet.")
            no_comments_label.setAlignment(Qt.AlignCenter)
            no_comments_label.setStyleSheet("color: #888888; font-style: italic; padding: 20px;")
            self.comments_container_layout.addWidget(no_comments_label)
            return
        
        sorted_comments = sorted(self.bug.comments, 
                                key=lambda x: x.get('created_at', ''), 
                                reverse=True)
        
        for comment in sorted_comments:
            author = comment.get('author', 'Unknown')
            text = comment.get('text', '')
            created_at = comment.get('created_at', '')
            
            if created_at:
                date_str = created_at[:19].replace('T', ' ')
            else:
                date_str = "Unknown date"
            
            comment_widget = QWidget()
            comment_widget.setStyleSheet("""
                QWidget {
                    background-color: #2a2a2a;
                    border-radius: 5px;
                    border: 1px solid #444;
                }
            """)
            
            comment_layout = QVBoxLayout()
            comment_layout.setContentsMargins(10, 10, 10, 10)
            comment_layout.setSpacing(5)
            
            header_layout = QHBoxLayout()
            
            author_label = QLabel(f"👤 {author}")
            author_label.setStyleSheet("color: #4a9eff; font-weight: bold;")
            header_layout.addWidget(author_label)
            
            header_layout.addStretch()
            
            date_label = QLabel(date_str)
            date_label.setStyleSheet("color: #888888; font-size: 10px;")
            header_layout.addWidget(date_label)
            
            comment_layout.addLayout(header_layout)
            
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setStyleSheet("color: #444;")
            comment_layout.addWidget(separator)
            
            comment_text = QLabel(text)
            comment_text.setWordWrap(True)
            comment_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
            comment_text.setStyleSheet("""
                QLabel {
                    color: #e0e0e0;
                    padding: 5px 0px;
                    font-size: 11px;
                }
            """)
            
            if len(text) > 300:
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setMaximumHeight(150)
                scroll_area.setStyleSheet("""
                    QScrollArea {
                        border: none;
                        background-color: transparent;
                    }
                    QScrollArea > QWidget > QWidget {
                        background-color: transparent;
                    }
                """)
                
                text_widget = QWidget()
                text_layout = QVBoxLayout()
                text_layout.addWidget(comment_text)
                text_widget.setLayout(text_layout)
                scroll_area.setWidget(text_widget)
                comment_layout.addWidget(scroll_area)
            else:
                comment_layout.addWidget(comment_text)
            
            comment_widget.setLayout(comment_layout)
            
            spacer = QWidget()
            spacer.setFixedHeight(5)
            self.comments_container_layout.addWidget(comment_widget)
            self.comments_container_layout.addWidget(spacer)