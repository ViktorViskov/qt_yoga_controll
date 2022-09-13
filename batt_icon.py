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
        result = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/percentage/' | awk '{print $2}'").read().strip()
        # result = open("/sys/class/power_supply/BAT1/capacity", "r").read()

        # check for result is exist
        if result:
            result = result.split("%")[0]
        else:
            result = "0"

        # send signal
        self.out.emit(result)
        sleep(5)

class batt_icon(QIcon):
    def __init__(self, bat_status:str) -> None:
        super().__init__()

        # preparing
        pixmap = QPixmap(128, 128)
        pixmap.fill(QColor(0,0,0,255))

        # painter
        painter = QPainter(pixmap)

        # define color for paint
        number = int(bat_status)
        if number <= 10:
            color = QColor(127,0,0,255)
        elif number <= 20:
            color = QColor(255,0,0,255)
        elif number <= 35:
            color = QColor(255,127,0,255)
        elif number <= 50:
            color = QColor(150,150,0,255)
        else:
            color = QColor(0,127,0,255)

        # create pen for painting battery
        pen = QPen(color)
        pen.setWidth(4)
        painter.setPen(pen)

        # battery body
        painter.drawRoundedRect(2,32,119,64, 8, 8)
        painter.drawLine(126,50,126, 78)

        # fill battery
        painter.fillRect(4,34,round(1.15 * number),60, color)

        # write percents
        pen.setColor(QColor("white"))
        painter.setPen(pen)
        painter.setFont( QFont("Liberation Mono", 40, 70) )

        # for 1 char
        if len(bat_status) == 1:
            painter.drawText( QPoint(44, 82), bat_status)

        if len(bat_status) == 2:
            # for 2 char
            painter.drawText( QPoint(25, 82), bat_status)

        if len(bat_status) == 3:
            # for 3 chars
            painter.drawText( QPoint(9, 82), bat_status)
        

        # stop drawing
        painter.end()
        self.addPixmap(pixmap)

