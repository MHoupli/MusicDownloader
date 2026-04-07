from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem
from pytubefix import YouTube, Search
from pydub import AudioSegment
import os

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Welcome to my music downloader!\nYou can download music from YouTube by entering the URL or searching for it by name.")
        layout.addWidget(label)
        layout.addWidget(QLabel("Enter the destination directory:"))
        dir_layout = QHBoxLayout()
        self.dir_line_edit = QLineEdit()
        self.dir_line_edit.setReadOnly(True)
        self.dir_line_edit.setText("Select a directory to save your music")
        dir_layout.addWidget(self.dir_line_edit)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self._open_dir_dialog())
        dir_layout.addWidget(browse_button)
        layout.addLayout(dir_layout)
        layout.addWidget(QLabel("Enter the URL of the music you want to download:"))
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter the URL of the music you want to download")
        layout.addWidget(self.line_edit)
        layout.addWidget(QLabel("Or search for music by name:"))
        search_layout = QHBoxLayout()
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Search by video name")
        search_layout.addWidget(self.search_line_edit)
        search_button = QPushButton("Search")
        search_button.clicked.connect(lambda: self._search_music())
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)
        self.search_table = QTableWidget()
        self.search_table.itemClicked.connect(lambda item: self._handle_item_click(item))
        self.search_table.hide()
        self.search_table.setColumnWidth(0, 450)
        self.search_table.setColumnWidth(1, 150)
        self.searches = []
        layout.addWidget(self.search_table)
        layout.addStretch()
        self.status = QLabel("")
        download_button = QPushButton("Download Music")
        download_button.clicked.connect(lambda: self._download_music())
        layout.addWidget(self.status)
        layout.addWidget(download_button)

    def _open_dir_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.dir_line_edit.setText(dir_path)

    def _download_music(self):
        if self.dir_line_edit.text() == "Select a directory to save your music":
            print("Please select a valid directory.")
            self.status.setText("Please select a valid directory.")
            return
        elif self.line_edit.text() == "":
            print("Please enter a valid URL.")
            self.status.setText("Please enter a valid URL.")
            return
        URL = self.line_edit.text()
        video = YouTube(URL)
        self.status.setText(f"Downloading: {video.title}")
        audio = video.streams.get_audio_only()
        audio.download(output_path=self.dir_line_edit.text())
        audio_path = f"{self.dir_line_edit.text()}/{video.title}.m4a"
        mp3_path = f"{self.dir_line_edit.text()}/{video.title}.mp3"
        AudioSegment.from_file(audio_path).export(mp3_path, format="mp3")
        self.status.setText(f"Download completed: {video.title}")
        os.remove(audio_path)

    def _search_music(self):
        self.search_table.clearContents()
        self.searches = []
        if self.search_line_edit.text() == "":
            self.search_table.hide()
            return
        else:
            self.search_table.show()
            query = self.search_line_edit.text()
            num_items = min(10, len(Search(query).videos))
            search = Search(query).videos[:num_items]
            self.search_table.setRowCount(len(search))
            self.search_table.setColumnCount(2)
            self.search_table.setHorizontalHeaderLabels(["Title", "Duration"])
            for i, result in enumerate(search):
                self.search_table.setItem(i, 0, QTableWidgetItem(result.title))
                self.search_table.setItem(i, 1, QTableWidgetItem(str(result.length)))
                self.searches.append(result.watch_url)

    def _handle_item_click(self, item):
        self.line_edit.setText(self.searches[item.row()])