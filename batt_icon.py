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

        # check for result is exist
        if result:
            result = result.split("%")[0]
        else:
            result = "0"

        # send signal
        self.out.emit(result)
        sleep(1)

class batt_icon(QIcon):
    def __init__(self, bat_status:str) -> None:
        super().__init__()

        # preparing
        pixmap = QPixmap(128, 128)
        pixmap.fill(QColor(0,0,0,0))

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
        painter.drawRoundedRect(2,32,123,64, 8, 8)
        painter.drawLine(507,220,507, 280)

        # painter.drawRect(0,43,128,43)
        # pen.setWidth(50)
        # painter.setPen(pen)


        # fill
        # painter.fillRect(30,110,4.38 * number,292, color)
        # painter.drawR


        # title
        # pen.setColor(QColor("white"))
        # painter.setPen(pen)
        # painter.setFont( QFont("Liberation Mono", 170, 70) )

        # # for 1 char
        # if len(bat_status) == 1:
        #     painter.drawText( QPoint(170, 330), bat_status)

        # if len(bat_status) == 2:
        #     # for 2 char
        #     painter.drawText( QPoint(100, 330), bat_status)

        # if len(bat_status) == 3:
        #     # for 3 chars
        #     painter.drawText( QPoint(35, 330), bat_status)
        

        # stop drawing
        painter.end()
        self.addPixmap(pixmap)

