from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget(QWidget):
    app: QApplication
    # layout: QVBoxLayout
    label: QPushButton
    mousepos = QCursor.pos()

    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        sad = QPixmap()
        QS
        self.layout = QVBoxLayout(self)
        self.label = QPushButton("Print")
        self.label.mousePressEvent = lambda event: print(self.parent.pos)
        self.layout.addWidget(self.label)
        self.move(self.parent.pos)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)



