import appdaemon.plugins.hass.hassapi as hass
from enum import Enum
from machine import Machine, ANY, StateEq, StateNeq, Timeout

class States(Enum):
    DOOR_OPEN = 1
    DOOR_CLOSED = 2
globals().update(States.__members__) # Make the states accessible without the States. prefix.


class VolumeControl(hass.Hass):
    def initialize(self):
        #Get the TV and speaker entities
        self.living_room_tv = self.get_entity("media_player.samsung_7_series_55")
        self.living_room_speaker = self.get_entity("media_player.sonos_living_room")
        machine = Machine(self, states = States, initial = DOOR_CLOSED)

        machine.add_transition(DOOR_CLOSED, StateEq('binary_sensor.kitchen_window', 'on'), DOOR_OPEN, on_transition=self.reduce_volume)
        machine.add_transition(DOOR_OPEN, StateEq('binary_sensor.kitchen_window', 'off'), DOOR_CLOSED, on_transition=self.restore_volume)
        
        machine.log_graph_link()

    def reduce_volume(self):
        # e.g. Remember the current volume setting.
        self.log("Reducing the volume of TV & Speaker")
        self.tv_volume = self.living_room_tv.get_state(attribute = "volume_level")
        self.speaker_volume = self.living_room_speaker.get_state(attribute = "volume_level")
        str = f"Saving TV volume: {self.tv_volume}, speaker volume: {self.speaker_volume} "
        self.log(str, ascii_encode=False)

        #Set to lower volumes         
        self.living_room_tv.call_service("volume_set", volume_level = 0.1)       
        self.living_room_speaker.call_service("volume_set", volume_level = 0.1)
        str = f"Setting TV volume: 0.1 , speaker volume: 0.1 "
        self.log(str, ascii_encode=False)

    def restore_volume(self):
        self.log("Restoring the volume of TV & Speaker")
        self.living_room_tv.call_service("volume_set", volume_level = self.tv_volume)       
        self.living_room_speaker.call_service("volume_set", volume_level = self.speaker_volume)
        str = f"Setting TV volume: {self.tv_volume}, speaker volume: {self.speaker_volume} "
        self.log(str, ascii_encode=False)