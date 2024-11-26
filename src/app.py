import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QTimer


class MyApp(QWidget):
    def __init__(self):
        self.filepath = "D:\\Nagrania praca inzynierska\\Obrobione\\30.mp4"
        self.options_label_text = ""
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

        # WIDGET OPCJE APLIKACJI
        options_layout = QVBoxLayout()
        self.options_label = QLabel("")
        options_layout.addWidget(self.options_label)

        choose_file_button = QPushButton("Wybierz plik do analizy")
        choose_file_button.clicked.connect(self.choose_file)
        self.options_label.setText(self.options_label_text)
        options_layout.addWidget(choose_file_button)

        play_video_button = QPushButton("Uruchom analizę")
        play_video_button.clicked.connect(self.play_video)
        options_layout.addWidget(play_video_button)

        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        grid.addWidget(options_widget, 0, 0)

        # WIDGET VIDEO PLAYER
        self.videoWidget = QVideoWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.videoWidget)
        grid.addLayout(vbox, 0, 1)

        # WIDGET EMPTY
        grid.addWidget(QLabel(""), 0, 2)

        self.timer_label = QLabel("Elapsed Time: 0s")
        grid.addWidget(self.timer_label, 1, 0)
        # Set up a timer to update the timer label
        self.elapsed_seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        

        grid.addWidget(QLabel("Analiza strefy oczekiwania"), 1, 1)
        grid.addWidget(QLabel("Wyniki"), 1, 2)

        # Set up the video player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Set the main window properties
        self.setWindowTitle("2x3 Grid Layout with Video Player")
        self.setGeometry(100, 100, 1600, 900)
        self.show()

    def play_video(self):
        # video_url = QUrl.fromLocalFile(
        #     "D:/Nagrania praca inzynierska/Obrobione/30.mp4"
        # )
        video_url = QUrl.fromLocalFile(self.filepath)
        self.mediaPlayer.setMedia(QMediaContent(video_url))
        self.mediaPlayer.play()
        # Uruchom timer
        self.elapsed_seconds = 0
        self.timer.start(10)  # Update every 10ms

    def update_timer(self):
        # Increment elapsed time and update the timer label
        self.elapsed_seconds += 0.01
        self.timer_label.setText(f"Elapsed Time: {self.elapsed_seconds:.2f}s")

    def choose_file(self):
        # Open a file dialog to choose a video file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik do analizy", "", "Pliki wideo (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            self.filepath = file_path
            print(f"Wybrany plik: {file_path}")
        self.options_label.setText(f"Wybrano plik: {file_path}")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_func = MyApp()
    app_func.play_video()
    sys.exit(app.exec_())
