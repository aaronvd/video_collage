from collage import collage
from video_player import video_player
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QStyle
import shutil
import time

class CollageProgram():
    def __init__(self, collage, videoplayer):

        self.collage = collage
 
        self.videoplayer = videoplayer
        self.videoplayer.resize(640, 480)
        self.videoplayer.show()

        self.widget = QWidget()
        self.button1 = QPushButton(self.widget)
        # self.button1 = QPushButton('Test', self.widget)
        self.button1.setIcon(self.widget.style().standardIcon(QStyle.SP_DialogNoButton))
        self.button1.resize(200,175)
        self.button1.move(60,13)
        self.button1.clicked.connect(self.button1_clicked)
        self.widget.setGeometry(600,600,320,200)
        self.widget.setWindowTitle("Record video")
        self.widget.show()
        sys.exit(app.exec_())

    def button1_clicked(self):
        self.button1.hide()
        print("Recording...")
        self.collage.record()
        print("Building collage...")
        self.collage.build_collage()
        self.videoplayer.stop()
        time.sleep(5)
        shutil.copy('../Videos/collage_temp.avi', '../Videos/collage.avi')
        self.videoplayer.play()
        self.button1.show()
        print("Ready to record.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    collage = collage(color_type='tile', length_seconds=5)
    videoplayer = video_player(fileName='../Videos/collage.avi')
    
    CollageProgram(collage, videoplayer)
   




