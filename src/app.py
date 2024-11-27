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
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, QTimer
import pandas as pd
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time


from yolo_annotator import yolo_model
from algorithms_time import time_algorithms


class MyApp(QWidget):
    def __init__(self):
        self.filepath = "D:\\Nagrania praca inzynierska\\Obrobione\\30.mp4"
        self.options_label_text = ""
        self.dataset_path = "Dataset.xlsx"
        self.sheet_name_single_cross = "Jednostkowy czas przejścia"
        self.sheet_name_group_cross = "Czas przejścia grupy"
        self.data_group_corss = self.read_xlsx_sheet(
            self.dataset_path, self.sheet_name_group_cross
        )
        self.video_file_index = None
        self.yolo = yolo_model()
        self.algorithms = time_algorithms()
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
        self.options_label = QLabel("Wybierz plik wideo do analizy")
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

        # WIDGET WIZUALIZACJA
        bottom_left_grid = QGridLayout()
        self.timer_label = QLabel("Sekunda nagrania: 0")

        label_tree_algorithm = QLabel("Drzewo decyzyjne")
        label_tree_algorithm.setAlignment(Qt.AlignCenter)
        bottom_left_grid.addWidget(label_tree_algorithm, 0, 0)

        label_gauss_algorithm = QLabel("Algorytm autorski")
        label_gauss_algorithm.setAlignment(Qt.AlignCenter)
        bottom_left_grid.addWidget(label_gauss_algorithm, 0, 1)

        label_classic_algorithm = QLabel("Podejście klasyczne")
        label_classic_algorithm.setAlignment(Qt.AlignCenter)
        bottom_left_grid.addWidget(label_classic_algorithm, 0, 2)

        pixmap_tree = QPixmap("resources/Red.png")
        self.image_label_tree = QLabel("No Image")
        self.image_label_tree.setPixmap(pixmap_tree)
        self.image_label_tree.setAlignment(Qt.AlignCenter)
        self.image_label_tree.setStyleSheet("border: 1px solid black;")
        bottom_left_grid.addWidget(self.image_label_tree, 1, 0)

        pixmap_gauss = QPixmap("resources/Red.png")
        self.image_label_gauss = QLabel("No Image")
        self.image_label_gauss.setPixmap(pixmap_gauss)
        self.image_label_gauss.setAlignment(Qt.AlignCenter)
        self.image_label_gauss.setStyleSheet("border: 1px solid black;")
        bottom_left_grid.addWidget(self.image_label_gauss, 1, 1)

        pixmap_classic = QPixmap("resources/Red.png")
        self.image_label_classic = QLabel("No Image")
        self.image_label_classic.setPixmap(pixmap_classic)
        self.image_label_classic.setAlignment(Qt.AlignCenter)
        self.image_label_classic.setStyleSheet("border: 1px solid black;")
        bottom_left_grid.addWidget(self.image_label_classic, 1, 2)


        bottom_left_widget = QWidget()
        bottom_left_layout = QVBoxLayout()
        bottom_left_layout.addLayout(bottom_left_grid)
        bottom_left_layout.addWidget(self.timer_label)
        bottom_left_widget.setLayout(bottom_left_layout)
        grid.addWidget(bottom_left_widget, 1, 0)

        # Set up a timer to update the timer label
        self.elapsed_seconds = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)


        # WIDGET ZDJĘCIE WYNIK ANALIZY YOLO
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setAlignment(Qt.AlignCenter) 

        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label)

        image_widget = QWidget()
        image_widget.setLayout(image_layout)

        grid.addWidget(image_widget, 1, 1)

        wyniki_layout = QVBoxLayout()

        label_wyniki = QLabel("Wyniki")
        wyniki_layout.addWidget(label_wyniki)

        self.label_start_zielonego = QLabel("Zielone światło zaczęło się sekundzie: 0")
        wyniki_layout.addWidget(self.label_start_zielonego)

        self.label_czas_przechodzenia = QLabel("Przechodnie przeszli przejście w 0s")
        wyniki_layout.addWidget(self.label_czas_przechodzenia)

        self.label_wynik_tree = QLabel("Predykcja drzewa decyzyjnego:")
        wyniki_layout.addWidget(self.label_wynik_tree)

        self.label_wynik_gauss = QLabel("Predykcja algorytmu autorskiego:")
        wyniki_layout.addWidget(self.label_wynik_gauss)

        self.label_wynik_classic = QLabel("Podejście klasyczne:")
        wyniki_layout.addWidget(self.label_wynik_classic)

        self.label_błąd_absolutny_tree = QLabel("Błąd absolutny drzewa decyzyjnego:")
        wyniki_layout.addWidget(self.label_błąd_absolutny_tree)

        self.label_błąd_absolutny_gauss = QLabel("Błąd absolutny algorytmu autorskiego:")
        wyniki_layout.addWidget(self.label_błąd_absolutny_gauss)

        self.label_błąd_absolutny_classic = QLabel("Błąd absolutny klasycznego podejścia:")
        wyniki_layout.addWidget(self.label_błąd_absolutny_classic)

        self.label_czas_zagrożenia_tree = QLabel("Czas zagrożenia drzewa decyzyjnego:")
        wyniki_layout.addWidget(self.label_czas_zagrożenia_tree)

        self.label_czas_zagrożenia_gauss = QLabel("Czas zagrożenia algorytmu autorskiego:")
        wyniki_layout.addWidget(self.label_czas_zagrożenia_gauss)

        self.label_czas_zagrożenia_classic = QLabel("Czas zagrożenia klasycznego podejścia:")
        wyniki_layout.addWidget(self.label_czas_zagrożenia_classic)

        wyniki_widget = QWidget()
        wyniki_widget.setLayout(wyniki_layout)

        grid.addWidget(wyniki_widget, 1, 2)

        # Set up the video player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Set the main window properties
        self.setWindowTitle("Traffic light control support system")
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
        self.timer.start(10) #update every 10 ms
        if  self.video_file_index is not None:
            self.oblicz_wyniki()

    def update_timer(self):
        # Increment elapsed time and update the timer label
        self.elapsed_seconds += 0.01
        self.timer_label.setText(f"Sekunda nagrania: {self.elapsed_seconds:.2f}")
        self.update_lights()
    
    def update_lights(self):
        predictions = [self.decision_tree_time, self.gaus_time, 14]
        labels_lights = [self.image_label_tree, self.image_label_gauss, self.image_label_classic]
        
        for i in range(len(predictions)):
            if self.elapsed_seconds < self.czas_zielonego:
                pixmap = QPixmap("resources/Red.png")
                labels_lights[i].setPixmap(pixmap)
            elif self.elapsed_seconds >= self.czas_zielonego and predictions[i] + self.czas_zielonego >= self.elapsed_seconds:
                pixmap = QPixmap("resources/Green.png")
                labels_lights[i].setPixmap(pixmap)
            elif self.elapsed_seconds >= self.czas_zielonego and predictions[i] + self.czas_zielonego < self.elapsed_seconds and predictions[i] + 4 + self.czas_zielonego > self.elapsed_seconds:
                if self.elapsed_seconds - int(self.elapsed_seconds) < 0.5:
                    pixmap = QPixmap("resources/Green.png")
                    labels_lights[i].setPixmap(pixmap)
                else:
                    pixmap = QPixmap("resources/Off.png")
                    labels_lights[i].setPixmap(pixmap)
            else:
                pixmap = QPixmap("resources/Red.png")
                labels_lights[i].setPixmap(pixmap)

    def choose_file(self):
        # Open a file dialog to choose a video file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik do analizy", "", "Pliki wideo (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            self.filepath = file_path
        self.options_label.setText(f"Wybrano plik: {os.path.basename(file_path)}, rozpocznij analizę")
        self.video_file_index = int(os.path.splitext(os.path.basename(file_path))[0]) - 1 #pliki zaczynają się od 1 a index od 0

    def read_xlsx_sheet(self, file_path, sheet_name):
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return df
        except Exception as e:
            print(f"Error reading the Excel file: {e}")
            return None
    
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

    def oblicz_wyniki(self):
        czas_przejscia = self.data_group_corss.iloc[self.video_file_index]["Czas przechodzenia od zielonego"]
        self.czas_zielonego = self.data_group_corss.iloc[self.video_file_index]["Początek ZŚ"]
        klatka_zielonego = self.data_group_corss.iloc[self.video_file_index]["Początek zielonego światła klatka"]

        self.label_start_zielonego.setText(f"Zielone światło zaczęło się sekundzie: {self.czas_zielonego}")
        self.label_czas_przechodzenia.setText(f"Przechodnie przeszli przejście w {czas_przejscia:.2f}s")

        grupa_oczekujacych = self.yolo.create_annotated_image(self.filepath, klatka_zielonego)
        self.show_image()

        self.decision_tree_time = self.algorithms.predict_crossing_time_tree(grupa_oczekujacych)[0]
        self.gaus_time = self.algorithms.predict_crossing_time_gaus(grupa_oczekujacych)[0]

        self.label_wynik_tree.setText(f"Predykcja drzewa decyzyjnego: {self.decision_tree_time:.2f}s")
        self.label_wynik_gauss.setText(f"Predykcja algorytmu autorskiego: {self.gaus_time:.2f}s")
        self.label_wynik_classic.setText(f"Podejście klasyczne:{14}s")
        
        self.label_błąd_absolutny_tree.setText(f"Błąd absolutny drzewa decyzyjnego: {abs(self.decision_tree_time - czas_przejscia):.2f}s")
        self.label_błąd_absolutny_gauss.setText(f"Błąd absolutny algorytmu autorskiego: {abs(self.gaus_time - czas_przejscia):.2f}s")
        self.label_błąd_absolutny_classic.setText(f"Błąd absolutny klasycznego podejścia: {abs(14 - czas_przejscia):.2f}s")

        self.label_czas_zagrożenia_tree.setText(f"Czas zagrożenia drzewa decyzyjnego: {self.oblicz_czas_zagrozenia(czas_przejscia, self.decision_tree_time):.2f}s")
        self.label_czas_zagrożenia_gauss.setText(f"Czas zagrożenia algorytmu autorskiego: {self.oblicz_czas_zagrozenia(czas_przejscia, self.gaus_time):.2f}s")
        self.label_czas_zagrożenia_classic.setText(f"Czas zagrożenia klasycznego podejścia: {self.oblicz_czas_zagrozenia(czas_przejscia, 14):.2f}s")


    def oblicz_czas_zagrozenia(self, czas_przechodzenia_przechodniów, predykcja_czasu):
        if predykcja_czasu + 4 < czas_przechodzenia_przechodniów:
            czas_zagrozenia = czas_przechodzenia_przechodniów - (predykcja_czasu + 4)
        else:
            czas_zagrozenia = 0
        return czas_zagrozenia


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 15pt;}")
    app_func = MyApp()
    sys.exit(app.exec_())
