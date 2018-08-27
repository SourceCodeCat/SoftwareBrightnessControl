import sys
from os import path
from com.Display import DisplayManager

displayManager = DisplayManager()
displays = displayManager.getConnectedDisplays()
for d in displays:
    print("name:%s\nactive:%s\nbrightness:%.1f\nred:%.1f\nblue:%.1f\ngreen:%.1f\n\n" %\
     (d.name,d.active,d.brightness,d.red,d.blue,d.green))


#displays[0].brightness=0.5
#displays[0].red=0.25
#displays[0].green=0.50
#displays[0].green=0.75
#displayManager.changeAttributes(displays[0])