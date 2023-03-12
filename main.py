import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


# class Button(QPushButton):
#     def __init__(self):
#         super().__init__()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My App')

        button = QPushButton('Press Me!')
        button.clicked.connect(self.on_click)
        button.setFixedSize(QSize(100, 100))

        self.label = QLabel('Click in this window')

        self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(self.label)

    def on_click(self):
        print('Clicked!')

    def mouseMoveEvent(self, e):
        self.label.setText('mouseMoveEvent')


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec_()
