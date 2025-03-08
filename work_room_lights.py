import appdaemon.plugins.hass.hassapi as hass
import datetime
from at_home_trigger import at_home_event

class WorkRoomLights(hass.Hass):
    def initialize(self):
        self.work_room_motion = self.get_entity("binary_sensor.presenseworkroom")
        self.work_room_motion.listen_state(self.work_room_motion_light_on, new = "on")
        self.work_room_motion.listen_state(self.work_room_light_off, new = "off")

    def work_room_motion_light_on(self,  entity, attribute, old, new, kwargs):
        if self.trigger_event():        
            self.turn_on('light.workroom', brightness = 35, transition = 3)        

    
    def work_room_light_off(self,  entity, attribute, old, new, kwargs):
        self.turn_off('light.workroom', transition = 3)

    def trigger_event(self):
        #Trigger only when home and after sunset        
        if self.sun_entity.is_state('below_horizon'):
            return True
        else:
            return False
        