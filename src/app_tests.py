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
from PyQt5.QtGui import QPixmap
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

        # Add "Opcje aplikacji" widget with a button to choose a file
        options_layout = QVBoxLayout()
        options_label = QLabel("Opcje aplikacji")
        options_layout.addWidget(options_label)

        choose_file_button = QPushButton("Choose Video File")
        choose_file_button.clicked.connect(self.choose_file)
        options_layout.addWidget(choose_file_button)

        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        grid.addWidget(options_widget, 0, 0)

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

        grid.addWidget(QLabel("Opcje aplikacji"), 0, 2)
        grid.addWidget(QLabel("Wizualizacja algorytmów"), 1, 0)
        grid.addWidget(QLabel("Analiza strefy oczekiwania"), 1, 1)

        # Add the image display section in the bottom middle widget
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setAlignment(Qt.AlignCenter)  # Center align the image and text
        show_image_button = QPushButton("Show Image")
        show_image_button.clicked.connect(self.show_image)

        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(show_image_button)

        image_widget = QWidget()
        image_widget.setLayout(image_layout)
        grid.addWidget(image_widget, 2, 1)

        grid.addWidget(QLabel("Wyniki"), 1, 2)

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

        # Store the video file path
        self.video_file_path = None

        # Set the main window properties
        self.setWindowTitle(
            "2x3 Grid Layout with Video Player, Timer, and Image Display"
        )
        self.setGeometry(300, 300, 800, 500)  # Set size and position
        self.show()

    def choose_file(self):
        # Open a file dialog to choose a video file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            self.video_file_path = file_path
            print(f"Selected file: {file_path}")

    def play_video(self):
        if self.video_file_path:
            # Load the chosen video file into the media player
            video_url = QUrl.fromLocalFile(self.video_file_path)
            self.mediaPlayer.setMedia(QMediaContent(video_url))
            self.mediaPlayer.play()
        else:
            print("No video file selected. Please choose a file.")

    def update_timer(self):
        # Increment elapsed time and update the timer label
        self.elapsed_seconds += 1
        self.timer_label.setText(f"Elapsed Time: {self.elapsed_seconds}s")

    def show_image(self):
        # Load and display the image
        image_path = "results/inference.png"
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Failed to Load Image")
        else:
            self.image_label.setPixmap(
                pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
            )


if __name__ == "__main__":
    from PyQt5.QtCore import Qt  # Import here to prevent unused import error at top

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
