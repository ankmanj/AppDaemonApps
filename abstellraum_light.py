import appdaemon.plugins.hass.hassapi as hass
import datetime

class AbstellRaumLight(hass.Hass):
    def initialize(self):
        self.my_enitity = self.get_entity("binary_sensor.abstellraum_motion_sensor")      
        self.my_enitity.listen_state(self.motion_light_on, new = "on")
        self.my_enitity.listen_state(self.motion_light_off, new = "off")

        runtime = datetime.time(22, 00, 00)
        handle = self.run_daily(self.TurnOnLight, runtime)

        runtime = datetime.time(4, 15, 00)
        handle = self.run_daily(self.TurnOffLight, runtime)

    def motion_light_on(self,  entity, attribute, old, new, kwargs):
        if self.now_is_between("04:15:00", "22:00:00"):
            self.TurnOnLight(kwargs)
        
    def motion_light_off(self,  entity, attribute, old, new, kwargs):
        if self.now_is_between("04:15:00", "22:00:00"):
            self.TurnOffLight(kwargs)

    def TurnOnLight(self, kwargs):      
        str = f"before Turning on  lights"
        self.turn_on('light.abstellraumlight', brightness = 35,  transition = 3)                       
        str = f"Turning on lights"
        self.log(str, ascii_encode=False)
        
    def TurnOffLight(self, kwargs):
        self.turn_off('light.abstellraumlight', transition = 3)        
        str = f"Turning off  lights"
        self.log(str, ascii_encode=False)