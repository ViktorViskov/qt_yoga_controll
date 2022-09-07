# libs
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from widget import Widget

# main class for tray app
class Tray(QSystemTrayIcon):
    # varaibles
    app: QApplication
    pos: QPoint = None

    # widgets
    menu: QMenu
    window: Widget = None

    # actions
    exit: QAction

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app

        # config tray icon
        self.setIcon(QIcon("status.png"))
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
        self.exit.triggered.connect(self.app.quit)
        self.menu.addAction(self.exit)

    # show status widget
    def show_status(self, key_event):
        if key_event == 3:
            # check for window is show
            if not self.window:
                if not self.pos: 
                    self.pos = QCursor.pos()
                self.window = Widget(self)
                self.window.show()
                self.window.closeEvent = lambda event: self.show_status(3)
            else:
                self.pos = self.window.pos()
                self.window.closeEvent = None
                self.window.close()
                self.window = None




