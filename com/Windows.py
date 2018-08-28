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
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self,availableDisplays_,propertiesChangedCallback_):

        #save available displays.........
        self.availableDisplays = availableDisplays_
        self.currentSelectedDisplay = availableDisplays_[0] if len(availableDisplays_) > 0 else None

        #save callback ...
        self.propertiesChangedCallback = propertiesChangedCallback_

        #create main window and set layout..
        Gtk.Window.__init__(self,title="My Brightness Control")
        self.set_border_width(10)
        self.set_default_size(400, 300)
        #creating main window layout
        self.mainBoxLayout = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.mainBoxLayout.set_valign(Gtk.Align.START)
        self.add(self.mainBoxLayout)

        #create availableDisplay combo
        available_displays_store = Gtk.ListStore(str)
        for display in self.availableDisplays:
            available_displays_store.append([display.name])
        self.available_displays_combo = Gtk.ComboBox.new_with_model(available_displays_store)
        renderer_text = Gtk.CellRendererText()
        self.available_displays_combo.pack_start(renderer_text, True)
        self.available_displays_combo.add_attribute(renderer_text, "text", 0)        
        self.available_displays_combo.set_active(0)
        self.available_displays_combo.connect("changed", self.on_display_selected)
        

        #adding the displays combo to layout...        
        self.mainBoxLayout.pack_start(self.available_displays_combo, False, False, 0)      

        
        #create UI sliders...        
        self.brightness_scale = self.__createScale("Brightness",0.0,1.0,0.01,Gtk.Orientation.HORIZONTAL,self.on_disp_props_changed)
        self.mainBoxLayout.pack_start(self.brightness_scale, True, True, 0)

        self.gammaRed_scale = self.__createScale("Gamma_Red",0.1,1.0,0.01,Gtk.Orientation.HORIZONTAL,self.on_disp_props_changed)
        self.mainBoxLayout.pack_start(self.gammaRed_scale, True, True, 0)

        self.gammaGreen_scale = self.__createScale("Gamma_Green",0.1,1.0,0.01,Gtk.Orientation.HORIZONTAL,self.on_disp_props_changed)
        self.mainBoxLayout.pack_start(self.gammaGreen_scale, True, True, 0)        

        self.gammaBlue_scale = self.__createScale("Gamma_Blue",0.1,1.0,0.01,Gtk.Orientation.HORIZONTAL,self.on_disp_props_changed)
        self.mainBoxLayout.pack_start(self.gammaBlue_scale, True, True, 0)           

        # load the values of the first display in the combo
        self.setScaleValues(self.currentSelectedDisplay)

    #-------------------------------------------------------------------    
    #on combo selection....
    #-------------------------------------------------------------------    
    def on_display_selected(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            display = model[tree_iter][0]
            #print("Selected Display: %s\n" % display)
            for d in self.availableDisplays:
                if d.name == display:
                    self.currentSelectedDisplay = d
                    self.setScaleValues(d)

    #-------------------------------------------------------------------    
    #listen to changes in the display properties...
    #-------------------------------------------------------------------    
    def on_disp_props_changed(self,range,scroll,value):
        self.currentSelectedDisplay.brightness = self.brightness_scale.get_value()
        self.currentSelectedDisplay.red = self.gammaRed_scale.get_value()
        self.currentSelectedDisplay.green = self.gammaGreen_scale.get_value()
        self.currentSelectedDisplay.blue = self.gammaBlue_scale.get_value()
        self.propertiesChangedCallback(self.currentSelectedDisplay)    
    
    #-------------------------------------------------------------------    
    #This is a internal utility method... not intended to be used outside
    #  the Class
    #-------------------------------------------------------------------    
    def __createScale(self,name_,min_,max_,step_,orientation_,cb_):
        #creating the label for the scale and adding it to the layout...
        label = Gtk.Label()
        label.set_text(name_)
        label.set_halign(Gtk.Align.START)
        self.mainBoxLayout.pack_start(label, True, True, 0)
        #---------------------------------------------------------------
        #creating the scale....
        scale_ = Gtk.Scale.new_with_range(orientation_,min_, max_, step_)
        scale_.connect("change-value",cb_)
        scale_.set_inverted(False)
        scale_.set_name(name_)
        return scale_

    #-------------------------------------------------------------------    
    #Receives a display object so we can load the brightness and 
    # gamma props in the UI
    #-------------------------------------------------------------------    
    def setScaleValues(self,display):
        self.brightness_scale.set_value(display.brightness)
        self.gammaRed_scale.set_value(display.red)
        self.gammaGreen_scale.set_value(display.green)
        self.gammaBlue_scale.set_value(display.blue)


