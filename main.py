# SoftwareBrightnessControl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Brightness Controller is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Brightness Controller.  If not, see
# <http://www.gnu.org/licenses/>.
#Author: Marco Antonio Salgado Martinez

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