import appdaemon.plugins.hass.hassapi as hass
from threading import Event

#Define events
at_home_event = Event()

class FritzboxIphoneTracker(hass.Hass):
    def initialize(self):
        # Schedule this to run periodically or on demand
        self.iphone_barney_mac = self.args.get("iphone_barney_mac")
        self.iphone_sushi_mac = self.args.get("iphone_sushi_mac")

        self.log(f"Tracking iPhones: Barney ({self.iphone_barney_mac}), Sushi ({self.iphone_sushi_mac})", level="DEBUG")

        self.run_every(self.check_iphones, "now", 10)  # Every 10 seconds

    
    def check_iphones(self, kwargs):
        # Get all device trackers from Home Assistant
        device_trackers = self.get_state("device_tracker")        

        # Filter for Barney and Sushi's iPhones
        tracked_devices = {
            "Barney": self.find_device(self.iphone_barney_mac, device_trackers),
            "Sushi": self.find_device(self.iphone_sushi_mac, device_trackers),
        }
        

        # Log the tracking results
        for name, entity in tracked_devices.items():
            if entity:
                self.log(f"{name}'s iPhone is connected: {entity}", level="DEBUG")                
                at_home_event.set()
            else:
                self.log(f"{name}'s iPhone is not connected.", level="DEBUG")
                at_home_event.clear()

    def find_device(self, mac_address, device_trackers):
        """Helper function to find a device by MAC address."""        
        for entity, attributes in device_trackers.items():
            if attributes.get("attributes").get("mac") == mac_address:
                return entity
        return None
