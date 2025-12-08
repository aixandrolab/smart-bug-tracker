import sys
from PyQt5.QtWidgets import QApplication
from core.main import MainWindow

def apply_dark_theme(app):
    app.setStyle("Fusion")
    
    dark_stylesheet = """
    QMainWindow {
        background-color: #2b2b2b;
    }
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QLabel {
        color: #ffffff;
    }
    QPushButton {
        background-color: #3c3c3c;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 8px 16px;
        color: #ffffff;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #4a4a4a;
        border: 1px solid #666666;
    }
    QPushButton:pressed {
        background-color: #2d2d2d;
    }
    QPushButton#helpButton {
        background-color: #2d4a6e;
    }
    QPushButton#exitButton {
        background-color: #6e2d2d;
    }
    QPushButton#exitButton:hover {
        background-color: #8a3a3a;
    }
    """
    
    app.setStyleSheet(dark_stylesheet)

def main():
    app = QApplication(sys.argv)
    
    apply_dark_theme(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()