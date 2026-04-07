from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit
from main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Downloader")
        self.setFixedSize(600, 300)
        self.setCentralWidget(MainWidget())
