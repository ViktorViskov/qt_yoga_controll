from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget(QWidget):
    app: QApplication
    # layout: QVBoxLayout
    label: QLabel

    def __init__(self) -> None:
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Hello")
        self.layout.addWidget(self.label)
        self.move(QCursor.pos())
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(300,100)

