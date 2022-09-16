# libs
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
from os import popen
from os.path import exists

# worker for update battery icon
class batt_worker(QThread):
    out = pyqtSignal(str, bool)
    def  __init__(self, parent = None):
        QThread.__init__(self, parent=parent)

    # worker body
    def run(self):
      while True:
        # result = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/percentage/' | awk '{print $2}'").read().strip()
        # try to get batt status
        if exists("/sys/class/power_supply/BAT1/capacity"):
            mode = open("/sys/class/power_supply/BAT1/capacity", "r").read()
            # check for chargering
            mode = True
        else:
            mode = False

        # try to get batt level
        if exists("/sys/class/power_supply/BAT1/capacity"):
            level = open("/sys/class/power_supply/BAT1/capacity", "r").read()
        else:
            level = "0"

        # send signal
        self.out.emit(level, mode)
        sleep(5)

class batt_icon(QIcon):
    def __init__(self, bat_status:str, mode:bool) -> None:
        super().__init__()

        # preparing
        pixmap = QPixmap(128, 128)
        pixmap.fill(QColor(0,0,0,0))

        # painter
        painter = QPainter(pixmap)

        # if charging add lighter
        if mode:
            charg_pen = QPen(QColor(255,255,0,255))
            charg_brush = QBrush(QColor(255,255,0,255))
            painter.setPen(charg_pen)
            painter.setBrush(charg_brush)

            # charging icon
            lighter = QPolygonF([ QPoint(96,2), QPoint(12,74), QPoint(60,60), QPoint(32,126), QPoint(116,54), QPoint(68,68)])
            painter.drawPolygon(lighter)


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
        brush = QBrush()
        painter.setPen(pen)
        painter.setBrush(brush)

        # battery body
        painter.fillRect(4,34,110,60, QColor(0,0,0,108))
        painter.drawRoundedRect(2,32,114,64, 8, 8)
        pen.setWidth(10)
        painter.setPen(pen)
        painter.drawLine(123,55,123, 73)

        # fill battery
        painter.fillRect(4,34,round(1.1 * number),60, color)

        # write percents
        pen.setColor(QColor("white"))
        painter.setPen(pen)
        painter.setFont( QFont("Liberation Mono", 42, 70) )

        # for 1 char
        if len(bat_status) == 1:
            painter.drawText( QPoint(44, 83), bat_status)

        if len(bat_status) == 2:
            # for 2 char
            painter.drawText( QPoint(25, 83), bat_status)

        if len(bat_status) == 3:
            # for 3 chars
            painter.drawText( QPoint(10, 83), bat_status)
        

        # stop drawing
        painter.end()
        self.addPixmap(pixmap)

class batt_window(QWidget):
    app: QApplication
    layout: QVBoxLayout
    button: QPushButton
    label: QLabel
    mousepos = QCursor.pos()

    def __init__(self, parent) -> None:
        # init widget
        super().__init__()
        self.setFixedSize(300,200)

        self.parent = parent
        self.layout = QVBoxLayout(self)

        # label with description
        self.description = QLabel("Path to battery \nExample /sys/class/power_supply/BAT1/")
        self.layout.addWidget(self.description)

        # input field
        self.input_field = QLineEdit()
        self.input_field.setText("/sys/class/power_supply/BAT1/")
        self.layout.addWidget(self.input_field)

        # save button
        self.button = QPushButton("Save")
        self.button.mousePressEvent = lambda event: print(self.input_field.text())
        self.layout.addWidget(self.button)

        # if exist saved position, move to this position
        # if self.parent.pos:
            # self.move(self.parent.pos)
        # self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(  Qt.WindowType.Dialog)


    def change_label(self):
        result = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/percentage/' | awk '{print $2}'").read()

# main class for tray app
class batt_tray(QSystemTrayIcon):
    # varaibles
    app: QApplication
    pos: QPoint = None
    battery_level = ""
    b_worker: batt_worker

    # widgets
    menu: QMenu
    window: batt_window = None

    # actions
    exit: QAction

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app

        # config tray icon and create worker
        self.setIcon(batt_icon("0", False))
        self.b_worker = batt_worker(self)
        self.b_worker.out.connect(self.update_battery_icon)
        self.b_worker.start()

        self.setVisible(True)

        # create menu
        self.create_menu()

        # adding menu
        self.setContextMenu(self.menu)

        # show window on click
        self.activated.connect(self.show_status)

    # method for create menu
    def create_menu(self):
        self.menu = QMenu()

        # create actions
        self.exit = QAction("Quit")
        self.exit.triggered.connect(self.app_quit)
        self.menu.addAction(self.exit)

    # show status widget
    def show_status(self, key_event):
        if key_event == 3:
            # check for window is show
            if not self.window:
                if not self.pos: 
                    #  define window size
                    # self.pos = QCursor.pos()
                    pass
                #     window_size = QDesktopWidget().screenGeometry()
                #     self.pos = QPoint(window_size.width() - (window_size.width() - 300),window_size.height() - (window_size.height() - 100))
                self.window = batt_window(self)
                self.window.show()
                self.window.closeEvent = lambda event: self.show_status(3)
            else:
                self.pos = self.window.pos()
                self.window.closeEvent = None
                self.window.close()
                self.window = None
        
        elif key_event == 4:
            self.app_quit()


    # method for update buttery icon
    def update_battery_icon(self, new_battery_level: str, mode: bool):
        # check for new data
        if self.battery_level != new_battery_level:
            # change icon
            self.setIcon(batt_icon(new_battery_level, mode))
            
            # set info about time to empty
            message = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/percentage/'").read().strip()

            # check for message is exist
            if not message:
                message = "Can not read data about battery"
            
            self.setToolTip(message)

        # replace battery level
        self.battery_level = new_battery_level

    # method for safe close app
    def app_quit(self):
        self.b_worker.terminate()
        self.b_worker.finished.connect(self.app.quit)


