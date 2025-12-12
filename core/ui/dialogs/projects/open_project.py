import os

from PyQt5.QtWidgets import QFileDialog


class OpenProjectDialog(QFileDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open project")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter("Smart Bug Tracker (*.bugtracker.json)")
        self.setViewMode(QFileDialog.Detail)
        
        self.setDirectory(os.path.expanduser("~"))
