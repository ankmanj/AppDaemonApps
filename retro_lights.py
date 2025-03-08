import appdaemon.plugins.hass.hassapi as hass
import datetime
from Iphone_presence import at_home_event


class RetroLightOn(hass.Hass):
    def initialize(self):
        self.run_at_sunset(self.TurnOnLight)
        runtime = datetime.time(23, 00, 00)
        handle = self.run_daily(self.TurnOffLight, runtime)

        #Turn on light at 04.30am morning and turn off at 07.15am 
        runtime = datetime.time(4, 30, 00)
        handle = self.run_daily(self.LivingRoomLampOn, runtime)

        runtime = datetime.time(7, 15, 00)
        handle = self.run_daily(self.LivingRoomLampOff, runtime)
        
        #Turn on lights after late night if motion detected
        self.living_room_motion_enitity = self.get_entity("binary_sensor.living_room_motion")
        self.living_room_motion_enitity.listen_state(self.MotionLightsOn, new = "on")
        self.living_room_motion_enitity.listen_state(self.MotionLightsOff, new = "off")
        
    def TurnOnLight(self, kwargs):
        if at_home_event.wait():
            self.log("Turning retro lights on")
            self.log("Event at_home_event :" + str(at_home_event.is_set()))
            self.turn_on('light.living_room_retro_bulb_1', brightness = 45, transition = 3)
            self.turn_on('light.living_room_retro_bulb_2', brightness = 45, transition = 3)
            self.turn_on('light.living_room_retro_bulb_3', brightness = 45, transition = 3)
            self.turn_on('light.living_room_retro_bulb_4', brightness = 45, transition = 3)

        
    def TurnOffLight(self, kwargs):
        self.log("Turning retro lights off")
        self.turn_off('light.living_room_retro_bulb_1', transition = 3)
        self.turn_off('light.living_room_retro_bulb_2', transition = 3)
        self.turn_off('light.living_room_retro_bulb_3', transition = 3)
        self.turn_off('light.living_room_retro_bulb_4', transition = 3)

    def MotionLightsOn(self,  entity, attribute, old, new, kwargs):
        self.log("Living room motion detected!")
        if self.now_is_between("23:00:00", "05:40:00"):
            self.TurnOnLight(kwargs)
        
        
    def MotionLightsOff(self,  entity, attribute, old, new, kwargs):
        self.log("Living room motion UNdetected!")
        if self.now_is_between("23:00:00", "05:40:00"):
            self.TurnOffLight(kwargs)

    def LivingRoomLampOn(self, kwargs):
            if at_home_event.wait():
                self.log("Turning On Living room lamp")
                self.turn_on('switch.living_room_lamp')

    def LivingRoomLampOff(self, kwargs):
        if at_home_event.wait():
            self.log("Turning Off Living room lamp")
            self.turn_off('switch.living_room_lamp')
    
