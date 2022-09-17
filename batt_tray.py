# libs
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
from os import popen
from os.path import exists, expanduser

# worker for update battery icon
class batt_worker(QThread):
    out = pyqtSignal(str, bool)
    path: str
    def  __init__(self, path: str ,parent = None):
        QThread.__init__(self, parent=parent)
        self.path = path

    # worker body
    def run(self):
      while True:
        # predefine variables
        mode = False
        level = "0"

        # try to get batt status
        if exists("%s/status" % (self.path)) and open("%s/status" % (self.path), "r").read().strip() == "Charging":
            mode = True

        # try to get batt level
        if exists("%s/capacity" % (self.path)):
            level = open("%s/capacity" % (self.path), "r").read().strip()

        # send signal
        self.out.emit(level, mode)
        sleep(5)

class batt_icon(QIcon):
    def __init__(self, bat_status:str, mode:bool) -> None:
        super().__init__()

        # preparing
        pixmap = QPixmap(128, 128)
        pixmap.fill(QColor(0,0,0,0))
        painter = QPainter(pixmap)

        # if charging add lighter
        if mode:
            charg_pen = QPen(QColor(0,0,0,255),3)
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
        elif number <= 30:
            color = QColor(255,127,0,255)
        elif number <= 40:
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

        # for 2 char
        if len(bat_status) == 2:
            painter.drawText( QPoint(25, 83), bat_status)

        # for 3 chars
        if len(bat_status) == 3:
            painter.drawText( QPoint(10, 83), bat_status)
        
        # stop drawing
        painter.end()
        self.addPixmap(pixmap)

class batt_window(QWidget):
    app: QApplication
    layout: QVBoxLayout
    button: QPushButton
    label: QLabel

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
        self.input_field.setText(self.parent.path)
        self.layout.addWidget(self.input_field)

        # save button
        self.button = QPushButton("Save")
        self.button.mousePressEvent = lambda event: self.save_event()
        self.layout.addWidget(self.button)

        # self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.Dialog)

    def save_event(self):
        self.parent.save_config(self.input_field.text())
        self.parent.start_worker()

        # close window
        self.close()

# main class for tray app
class batt_tray(QSystemTrayIcon):
    # varaibles
    app: QApplication
    pos: QPoint = None
    battery_level: str = ""
    battery_status: bool = False
    b_worker: batt_worker = None
    path: str = "/sys/class/power_supply/BAT1/"  #default path 

    # widgets
    menu: QMenu
    window: batt_window = None

    # actions
    exit: QAction

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app

        # load config file
        self.load_config()

        # config tray icon
        self.setIcon(batt_icon("0", False))
        self.setVisible(True)

        # start worker
        self.start_worker()

        # create menu and add menu
        self.create_menu()
        self.setContextMenu(self.menu)

        # show window on click
        self.activated.connect(self.show_status)

    # method for load user config file
    def load_config(self):
        user_directory = expanduser("~")
        if exists("%s/.config/pybatticon.conf" % user_directory):
            self.path = open("%s/.config/pybatticon.conf" % user_directory, "r").read()

    # method for save to config file
    def save_config(self, config_string:str):
        user_directory = expanduser("~")
        open("%s/.config/pybatticon.conf" % user_directory, "w").write(config_string)
        self.path = config_string

    
    # method for start and restart worker
    def start_worker(self):
        # terminate worker if exist
        if self.b_worker:
            self.b_worker.terminate()
            self.b_worker = None

        # create new worker
        self.b_worker = batt_worker(self.path, self)
        self.b_worker.out.connect(self.update_battery_icon)
        self.b_worker.start()

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
                self.window = batt_window(self)
                self.window.show()
                self.window.closeEvent = lambda event: self.show_status(3)
            else:
                self.window.closeEvent = None
                self.window.close()
                self.window = None
        
        # elif key_event == 4:
        #     self.app_quit()


    # method for update buttery icon
    def update_battery_icon(self, new_battery_level: str, mode: bool):
        # check for new data
        if self.battery_level != new_battery_level or self.battery_status != mode:
            # change icon
            self.setIcon(batt_icon(new_battery_level, mode))
            
            # set info about time to empty
            out = popen("upower -i /org/freedesktop/UPower/devices/DisplayDevice | awk '/time to /'").read().strip().capitalize().split(":")

            # message preparing
            if out:
                message = "%s: %s" % (out[0].strip(),out[1].strip())
            else:
                message = "Can not read data about battery"
            
            self.setToolTip(message)

        # replace battery level
        self.battery_level = new_battery_level
        self.battery_status = mode

    # method for safe close app
    def app_quit(self):
        self.b_worker.finished.connect(self.app.quit)
        self.b_worker.terminate()


