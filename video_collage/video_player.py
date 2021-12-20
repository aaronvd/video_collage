from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication,
                             QLabel, QFileDialog, QStyle, QVBoxLayout)

import sys
 
class video_player(QMainWindow):
    def __init__(self, fileName = 'collage.avi'):
        super().__init__()
        self.fileName = fileName
        #self.setWindowTitle("PyQt5 Video Player") 
        self.setWindowFlags(Qt.CustomizeWindowHint)
 
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        self.mediaPlayer.setPlaylist(self.playlist)
 
        widget = QWidget(self)
        self.setCentralWidget(widget)
 
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
 
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        
        self.mediaPlayer.play()
        
    def stop(self):
        self.mediaPlayer.stop()
        self.playlist.removeMedia(0)
        
    def play(self):
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        self.mediaPlayer.play()
 