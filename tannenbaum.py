import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class TannenbaumLights(hass.Hass):
    def initialize(self):
        #turn on lights
        runtime = datetime.time(16, 00, 00)
        handle = self.run_daily(self.tannenbaum_lights_on, runtime)

        #Turn off 
        runtime = datetime.time(20, 00, 00)
        handle = self.run_daily(self.tannenbaum_lights_off, runtime)   

    def tannenbaum_lights_on(self, kwargs):
        self.my_enitity = self.get_entity("switch.tannenbaum_plug")
        self.my_enitity.call_service("turn_on")

    
    def tannenbaum_lights_off(self,  entity, attribute, old, new, kwargs):
        self.my_enitity = self.get_entity("switch.tannenbaum_plug")
        self.my_enitity.call_service("turn_off")