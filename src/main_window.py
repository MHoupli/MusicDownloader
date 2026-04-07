from PySide6.QtWidgets import QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Downloader")
        self.setGeometry(100, 100, 800, 600)
