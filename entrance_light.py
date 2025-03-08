import appdaemon.plugins.hass.hassapi as hass
import datetime

class EntranceLight(hass.Hass):
    def initialize(self):
        self.my_enitity = self.get_entity("binary_sensor.entrancemotionsensor")        
        self.sun_entity = self.get_entity("sun.sun")
        self.my_enitity.listen_state(self.light_on, new = "on")
        self.my_enitity.listen_state(self.light_off, new = "off")
        
    def light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():
            str = f"before Turning on  lights"
            self.turn_on('light.entrance_retro_light_1', brightness = 35,  transition = 3)
            self.turn_on('light.entrance_retro_light_2', brightness = 35,  transition = 3)
            self.turn_on('light.entrance_retro_light_3', brightness = 35,  transition = 3)            
            str = f"Turning on lights"
            self.log(str, ascii_encode=False)
        
    def light_off(self,  entity, attribute, old, new, kwargs):
        self.turn_off('light.entrance_retro_light_1', transition = 3)
        self.turn_off('light.entrance_retro_light_2', transition = 3)
        self.turn_off('light.entrance_retro_light_3', transition = 3)
        str = f"Turning off  lights"
        self.log(str, ascii_encode=False)
        
    def trigger_event(self):
        #Trigger only when home and after sunset        
        if self.sun_entity.is_state('below_horizon'):
            return True
        else:
            return False
        