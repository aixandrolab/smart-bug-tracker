import sys
from PyQt5.QtWidgets import QApplication

from core.ui.windows.main_window import MainWindow
from core.utils.dark_theme import ModernDarkTheme

def main():
    app = QApplication(sys.argv)
    ModernDarkTheme.apply(app)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()