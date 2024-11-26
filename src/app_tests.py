import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up a grid layout
        grid = QGridLayout()
        self.setLayout(grid)

        # Add widgets to the grid layout with text from the diagram
        grid.addWidget(QLabel('Opcje aplikacji'), 0, 0)
        grid.addWidget(QLabel('Nagranie przejścia dla pieszych'), 0, 1)
        grid.addWidget(QLabel('Opcje aplikacji'), 0, 2)
        grid.addWidget(QLabel('Wizualizacja algorytmów'), 1, 0)
        grid.addWidget(QLabel('Analiza strefy oczekiwania'), 1, 1)
        grid.addWidget(QLabel('Wyniki'), 1, 2)

        # Set the main window properties
        self.setWindowTitle('2x3 Grid Layout Example')
        self.setGeometry(300, 300, 600, 400)  # Set size and position
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())