# libs
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
from os import popen

# worker for update battery icon
class batt_worker(QThread):
    out = pyqtSignal(str)
    def  __init__(self, parent = None):
        QThread.__init__(self, parent=parent)

    # worker body
    def run(self):
      while True:
        # Get time, date and day
        result = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/percentage/' | awk '{print $2}'").read().split("%")[0]

        # send signal
        self.out.emit(result)
        sleep(5)

class batt_icon(QIcon):
    def __init__(self, bat_status:str) -> None:
        super().__init__()

        # preparing
        pixmap = QPixmap("battery.png")

        # painting
        painter = QPainter(pixmap)

        # define color for paint
        number = int(bat_status)

        if number <= 10:
            painter.setPen(QColor(127,0,0,255))
        elif number <= 20:
            painter.setPen(QColor(255,0,0,255))
        elif number <= 35:
            painter.setPen(QColor(255,127,0,255))
        elif number <= 50:
            painter.setPen(QColor(150,150,0,255))
        else:
            painter.setPen(QColor(0,127,0,255))
            

        # title
        painter.setFont( QFont("Liberation Mono", 170, 70) )

        # for 1 char
        if len(bat_status) == 1:
            painter.drawText( QPoint(170, 330), bat_status)

        if len(bat_status) == 2:
            # for 2 char
            painter.drawText( QPoint(100, 330), bat_status)

        if len(bat_status) == 3:
            # for 3 chars
            painter.drawText( QPoint(35, 330), bat_status)
        

        # stop drawing
        painter.end()
        self.addPixmap(pixmap)

