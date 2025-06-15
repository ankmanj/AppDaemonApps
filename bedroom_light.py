import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class BedroomLight(hass.Hass):
    def initialize(self):
        self.bedroom_lamp = "light.bedroom"        
        
        self.run_at_sunset(self.night_lamp_on)
        self.run_at_sunrise(self.night_lamp_off)

        
    def bedroom_motion_light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():
            self.turn_on(in_brightness = 40)
        
    def bedroom_light_off(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():
            self.turn_off()
        
    def night_lamp_on(self, kwargs):
        self.log("Turning night lamp on", ascii_encode=False)
        self.turn_on(in_brightness=100)
        
    def night_lamp_off(self, kwargs):
        self.log("Turning night lamp off", ascii_encode=False)
        self.turn_off()
        
        
    def turn_on(self, in_brightness = 3):
        self.my_enitity = self.get_entity(self.bedroom_lamp)
        self.my_enitity.call_service("turn_on", brightness = in_brightness)
        str = f"Turning on bedroom lights"
        self.log(str, ascii_encode=False)
        
    def turn_off(self):
        self.my_enitity = self.get_entity(self.bedroom_lamp)
        self.my_enitity.call_service("turn_off")
        str = f"Turning off bedroom lights"
        self.log(str, ascii_encode=False)
        
        
    def trigger_event(self):
        if at_home_event.wait() and self.now_is_between("5:00:00", "23:00:00") and (float(self.bedroom_light_sensor.get_state()) < 30):
            return True
        else:
            return False
        
        