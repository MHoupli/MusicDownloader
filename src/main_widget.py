from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from pytubefix import YouTube
from pydub import AudioSegment
import os

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        label = QLabel("Welcome to my music downloader!")
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
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter the URL of the music you want to download")
        layout.addWidget(self.line_edit)
        download_button = QPushButton("Download Music")
        download_button.clicked.connect(lambda: self._download_music())
        layout.addWidget(download_button)

    def _open_dir_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.dir_line_edit.setText(dir_path)

    def _download_music(self):
        # Placeholder for download logic
        if self.dir_line_edit.text() == "Select a directory to save your music":
            print("Please select a valid directory.")
            return
        elif self.line_edit.text() == "":
            print("Please enter a valid URL.")
            return
        URL = self.line_edit.text()
        video = YouTube(URL)
        print(f"Downloading: {video.title}")
        audio = video.streams.get_audio_only()
        audio.download(output_path=self.dir_line_edit.text())
        print("Download completed!")
        print("Converting to MP3...")
        audio_path = f"{self.dir_line_edit.text()}/{video.title}.m4a"
        mp3_path = f"{self.dir_line_edit.text()}/{video.title}.mp3"
        AudioSegment.from_file(audio_path).export(mp3_path, format="mp3")
        print("Conversion completed!")
        os.remove(audio_path)  # Remove the original .m4a file
        print("Original file removed.")
