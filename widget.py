from random import random
from os import popen
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget(QWidget):
    app: QApplication
    layout: QVBoxLayout
    button: QPushButton
    label: QLabel
    mousepos = QCursor.pos()

    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.button = QPushButton("Print")
        self.button.mousePressEvent = lambda event: self.change_label()
        self.layout.addWidget(self.button)

        # self.move(self.parent.pos)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)


    def change_label(self):
        number = str(int(random() * 1000))
        result = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/percentage/' | awk '{print $2}'").read()



