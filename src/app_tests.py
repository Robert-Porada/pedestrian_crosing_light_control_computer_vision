import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up a grid layout
        grid = QGridLayout()
        self.setLayout(grid)

        # Adjust column stretch to make the middle column wider
        grid.setColumnStretch(0, 1)  # Left column
        grid.setColumnStretch(1, 3)  # Middle column (wider)
        grid.setColumnStretch(2, 1)  # Right column

        # Add widgets to the grid layout with text from the diagram
        grid.addWidget(QLabel('Opcje aplikacji'), 0, 0)

        # Add the video player to the top middle cell
        self.videoWidget = QVideoWidget()
        grid.addWidget(self.videoWidget, 0, 1)

        # Add play button for the video player
        play_button = QPushButton("Play Video")
        play_button.clicked.connect(self.play_video)
        vbox = QVBoxLayout()
        vbox.addWidget(self.videoWidget)
        vbox.addWidget(play_button)
        grid.addLayout(vbox, 0, 1)

        grid.addWidget(QLabel('Opcje aplikacji'), 0, 2)
        grid.addWidget(QLabel('Wizualizacja algorytmów'), 1, 0)
        grid.addWidget(QLabel('Analiza strefy oczekiwania'), 1, 1)
        grid.addWidget(QLabel('Wyniki'), 1, 2)

        # Add a timer label to the bottom left corner
        self.timer_label = QLabel("Elapsed Time: 0s")
        grid.addWidget(self.timer_label, 2, 0)

        # Set up a timer to update the timer label
        self.elapsed_seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every 1000ms (1 second)

        # Set up the video player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Set the main window properties
        self.setWindowTitle('2x3 Grid Layout with Video Player and Timer')
        self.setGeometry(300, 300, 800, 500)  # Set size and position
        self.show()

    def play_video(self):
        # Load a sample video file
        video_url = QUrl.fromLocalFile("sample_video.mp4")  # Replace with the path to your video
        self.mediaPlayer.setMedia(QMediaContent(video_url))
        self.mediaPlayer.play()

    def update_timer(self):
        # Increment elapsed time and update the timer label
        self.elapsed_seconds += 1
        self.timer_label.setText(f"Elapsed Time: {self.elapsed_seconds}s")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
