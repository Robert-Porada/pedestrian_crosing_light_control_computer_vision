import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl


class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.setWindowTitle("Nagranie przejścia dla pieszych")
        self.setGeometry(100, 100, 1600, 900)

        # Create a central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        

        # Create video widget
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        # Create media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget.setMaximumSize(700, 350)
        self.video_widget.setStyleSheet("background-color: black;")
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
        


    def play_video(self):
        self.media_player.play()


if __name__ == "__main__":
    video_path = "D:/Nagrania praca inzynierska/Obrobione/30.mp4"
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)
    player.show()
    player.play_video()
    sys.exit(app.exec_())
