import sys
import subprocess
from enum import Enum
import math
class Display(object):
    
    def __init__(self,name_):
        self.name = name_
        self.brightness = .0
        self.red = .0
        self.green = .0
        self.blue = .0
        self.active = False

class DisplayManager(object):


    def getConnectedDisplays(self):
        connected_displays = []
        try:        
            xrandr_result = self.execXrandrCommand('xrandr -q | grep -i "connected"')
            xrandr_result = xrandr_result.strip()
            #Python3 modification....--------------------------------
            # python3 sees this as a byte string...that's why we 
            # decode it to convert it to string type
            xrandr_result = xrandr_result.decode()
            #--------------------------------------------------------
            lines = xrandr_result.split('\n')
            for line in lines:
                words = line.split(' ')
                connected_displays.append(Display(words[0]))
                self.fillDisplayAttributes(connected_displays[-1])
        except:
            print("Error:"+sys.exc_info()[0]+"\n")
        return connected_displays


    def fillDisplayAttributes(self,display):
        str_ = self.execXrandrCommand("xrandr --verbose | grep "+display.name+" -A 5").strip()
        #Python3 modification....--------------------------------
        str_ = str_.decode()# converting from bytes to string...
        #--------------------------------------------------------
        disp_attrs = dict(self.decodeAttributeString(str_))
        
        #The dict contains more attributes but we are only interested in brightness and gamma
        if "Brightness" in disp_attrs:
            display.brightness = float(disp_attrs["Brightness"])
            gamma = disp_attrs["Gamma"].strip().split(":")
            display.red = float(gamma[0]) 
            display.green = float(gamma[1])
            display.blue = float(gamma[2])
            display.active = True
        

    def decodeAttributeString(self,str_):
        str_ = str_.strip().split('\n\t')[1:]
        l = []
        for attr in str_:
            try:
                k,v = attr.split(': ')
                l.append((k.strip(),v.strip()))
            except:
                print("problems decoding attribute: "+attr+"\n")
        return l

    def changeAttributes(self,display):
        str_ = "xrandr --output {0} --brightness {1} --gamma {2}:{3}:{4}"
        str_ = str_.format(display.name,display.brightness,display.red,display.green,display.blue)
        #print("command: "+str_)
        self.execXrandrCommand(str_)


    def execXrandrCommand(self,cmd):
        try:
            r = subprocess.check_output(cmd, shell=True)
            return r
        except:
            print("There was a problem executing the following (xrandr)command: %s\n returning en empty string...\n" % cmd)
            return ""