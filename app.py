import sys
from PyQt5.QtWidgets import QApplication

from core.dark_theme import ModernDarkTheme
from core.main import MainWindow

def main():
    app = QApplication(sys.argv)
    ModernDarkTheme.apply(app)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()