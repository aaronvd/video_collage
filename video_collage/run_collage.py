from collage import collage
from video_player import video_player
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QStyle
import shutil
import time

fileName = 'collage.avi'
   
def video_and_button_windows(videoplayer):
    
    videoplayer.resize(640, 480)
    videoplayer.show()
    
    widget = QWidget()
    button1 = QPushButton(widget)
    button1.setIcon(widget.style().standardIcon(QStyle.SP_DialogNoButton))
    button1.resize(200,175)
    button1.move(60,13)
    button1.clicked.connect(button1_clicked)
    widget.setGeometry(600,600,320,200)
    widget.setWindowTitle("Record video")
    widget.show()
    sys.exit(app.exec_())
   
def button1_clicked():
   print("Recording...")
   collage.record()
   print("Building collage...")
   collage.build_collage()
   videoplayer.stop()
   time.sleep(5)
   shutil.copy('collage_temp.avi', 'collage.avi')
   videoplayer.play()
   print("Ready to record.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    collage = collage(color_type='tile')
    videoplayer = video_player(fileName=fileName)
    
    video_and_button_windows(videoplayer)
   






