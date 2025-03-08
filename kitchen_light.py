import appdaemon.plugins.hass.hassapi as hass
import datetime

class KitchenLight(hass.Hass):
    def initialize(self):
        self.my_entity = self.get_entity("binary_sensor.kitchen_motion_sensor")      
        self.my_entity.listen_state(self.light_on, new = "on")
        self.my_entity.listen_state(self.light_off, new = "off")
        
    def light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():
            str = f"before Turning on Kitchen lights"
            self.call_service("switch/turn_on", entity_id = "switch.kitchenledstrip")
            str = f"Turning on Kitchen lights"
            self.log(str, ascii_encode=False)
        
    def light_off(self,  entity, attribute, old, new, kwargs):        
        self.call_service("switch/turn_off", entity_id = "switch.kitchenledstrip")
        str = f"Turning off Kitchen lights"
        self.log(str, ascii_encode=False)
        
    def trigger_event(self):
        #Trigger only when home and after sunset
        self.kitchen_light_sensor = self.get_entity("sensor.kitchen_motion_sensor")
        #10 is based on light measurements from 24.09.24 to 05.10.24
        if float(self.kitchen_light_sensor.get_state()) < 10:        
            return True
        else:
            return False
        