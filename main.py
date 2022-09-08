from inspect import trace
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from tray import Tray
  
# creating app
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
  
# creating tray
tray = Tray(app)
tray1 = Tray(app)
tray2 = Tray(app)
  
# Adding options to the System Tray
app.exec_()