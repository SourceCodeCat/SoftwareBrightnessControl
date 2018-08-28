import sys
from os import path
from com.Display import DisplayManager
from com.Windows import MainWindow
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


#retrieving the available displays-------------------
displayManager = DisplayManager()
displays = displayManager.getConnectedDisplays()
#----------------------------------------------------

#----------------------------------------------------
#this callback receives the changes in the currently 
# selected display 
#----------------------------------------------------   
def onPropertiesChanged(display):
    displayManager.changeAttributes(display)

#----------------------------------------------------
#instantiating a mainWindow object passing the available displays and the callback function
#in charge of receiving the changes in the display properties...
#----------------------------------------------------
mainWindowUI = MainWindow(displays,onPropertiesChanged)
mainWindowUI.connect("destroy",Gtk.main_quit)
mainWindowUI.show_all()
Gtk.main()