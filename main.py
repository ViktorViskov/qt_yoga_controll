from batt_tray import batt_tray
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
  
# creating app
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
  
# creating tray icons
battery = batt_tray(app)
  
# Adding options to the System Tray
app.exec_()