import appdaemon.plugins.hass.hassapi as hass
from at_home_trigger import at_home_event

Work = 16
Toilet = 17
Bathroom = 18
Storage = 19
Bedroom = 20
Kitchen = 21
Entrance = 22
Living_room = 23

class IphoneActions(hass.Hass):
    def initialize(self):
        handle = self.listen_event(self.IphoneGoodNight, event = "ios.action_fired")

    def IphoneGoodNight(self, event, data, kwargs): 
        self.log(data)       
        if(data['actionName'] == "Good night "):
            self.log("Good night, Turning off lights and Music")
            self.my_enitity = self.get_entity("light.living_room")
            self.my_enitity.call_service("turn_off", transition = 3)
            self.my_enitity = self.get_entity("light.kitchen")
            self.my_enitity.call_service("turn_off", transition = 3)
            self.my_enitity = self.get_entity("media_player.sonos_living_room")
            self.my_enitity.call_service("media_stop")
        if(data['actionName'] == "Work room light"):
            self.log("Toggle Work room lights")
            self.my_enitity = self.get_entity("light.workroom")
            self.my_enitity.call_service("toggle")
        if(data['actionName'] == "Living room lamp "):
            self.log("Toggle living room lamp")
            self.my_enitity = self.get_entity("switch.living_room_lamp")
            self.my_enitity.call_service("toggle")
        if(data['actionName'] == "Kitchen lamp"):
            self.log("Toggle kitchen lamp")
            self.my_entity = self.get_entity("light.kitchen")
            self.my_entity.call_service("toggle")
        if(data['actionName'] == "Living room lights"):
            self.log("Toggle living room lights")
            self.my_enitity = self.get_entity("light.living_room")
            self.my_enitity.call_service("toggle", brightness = 25)
        if(data['actionName'] == "Kitchen clean"):
            self.log("Cleaning Kitchen")
            self.my_entity = self.get_entity("vacuum.eufy")
            self.my_entity.call_service(service="send_command", command="app_segment_clean", params=[{"segments": [Kitchen], "repeat": 1}])            
        if(data['actionName'] == "Full Vacuum"):
            self.log("Vacuum Full house")
            self.my_entity = self.get_entity("vacuum.eufy")
            self.my_entity.call_service(service="send_command", command="app_start")