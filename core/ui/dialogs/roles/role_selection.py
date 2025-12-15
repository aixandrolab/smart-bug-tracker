from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound


class RoleSelectionDialog(QDialog):
    
    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Role")
        self.setFixedSize(400, 300)
        self.selected_role = None
        self.project_name = project_name

        self.click_sound = QSound('core/data/sounds/click.wav')
        self.notify_sound = QSound('core/data/sounds/notify.wav')
        self.error_sound = QSound('core/data/sounds/error.wav')
        
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
        developer_btn.clicked.connect(self.on_click)
        developer_btn.clicked.connect(lambda: self._select_role("developer"))
        developer_btn.setToolTip("Can create test tasks, view bugs, manage project versions")
        layout.addWidget(developer_btn)
        
        tester_btn = QPushButton("🧪 Tester")
        tester_btn.setMinimumHeight(60)
        tester_btn.clicked.connect(self.on_click)
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

    def on_click(self):
        self.click_sound.play()
    
    def on_notify(self):
        self.notify_sound.play()
    
    def on_error(self):
        self.error_sound.play()