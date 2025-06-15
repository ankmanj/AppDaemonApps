import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class WorkRoomLights(hass.Hass):
    def initialize(self):
        self.work_room_motion = self.get_entity("binary_sensor.presence_65")
        self.sun_entity = self.get_entity("sun.sun")
        self.work_room_motion.listen_state(self.work_room_motion_light_on, new = "on")
        self.work_room_motion.listen_state(self.work_room_light_off, new = "off")

        runtime = datetime.time(18, 00, 00)
        handle = self.run_daily(self.TurnOnLight, runtime)

        runtime = datetime.time(23, 00, 00)
        handle = self.run_daily(self.TurnOffLight, runtime)

    def work_room_motion_light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():        
            self.turn_on('light.work_room_lamp', brightness = 35, transition = 3)        

    
    def work_room_light_off(self,  entity, attribute, old, new, kwargs):
        self.turn_off('light.work_room_lamp', transition = 3)

    def trigger_event(self):
        #Trigger only when home and after sunset        
        if self.sun_entity.is_state('below_horizon'):
            return True
        else:
            return False

    def TurnOnLight(self, kwargs):      
        str = f"before Turning on  lights"
        self.turn_on('light.color_dimmable_light_4', brightness = 35,  transition = 3)                       
        str = f"Turning on lights"
        self.log(str, ascii_encode=False)
        
    def TurnOffLight(self, kwargs):
        self.turn_off('light.color_dimmable_light_4', transition = 3)        
        str = f"Turning off  lights"
        self.log(str, ascii_encode=False)
        