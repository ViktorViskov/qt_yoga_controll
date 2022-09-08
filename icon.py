# libs
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class custom_icon(QIcon):
    def __init__(self, title:str, subtitle:str) -> None:
        super().__init__()

        # preparing
        pixmap = QPixmap(64,64)
        color = QColor(0, 0, 0, 0)

        # background
        pixmap.fill(color)

        # painting
        painter = QPainter(pixmap)
        
        # title
        painter.setPen(QColor(0,255,0,255))
        painter.setFont( QFont("Liberation Mono", 22, 70) )
        painter.drawText( QPoint(4, 28), title)

        # subtext
        painter.setPen(QColor(0,255,0,255))
        painter.setFont( QFont("Liberation Mono", 18, 70) )
        painter.drawText( QPoint(10, 56), subtitle)

        # stop drawing
        painter.end()
        self.addPixmap(pixmap)

