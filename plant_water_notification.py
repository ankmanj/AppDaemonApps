import appdaemon.plugins.hass.hassapi as hass
from at_home_trigger import at_home_event
import datetime

class PlantWaterNotifier(hass.Hass):
    def initialize(self):
        self.notification_interval = 604800  # 1 week in seconds
        self.last_notification = None

        runtime = datetime.time(14, 0, 0)
        self.run_daily(self.check_season, runtime)   
        

    def check_season(self, kwargs):
        self.now = datetime.datetime.now()
        month = self.now.month
        if month in [12,1,2] :
            self.notification_interval = 1209600  # 2 weeks in seconds
        else:
            self.notification_interval = 604800  # 1 week in seconds
           
        if self.last_notification is None or (self.now - self.last_notification).total_seconds() > self.notification_interval:
            self.WaterPlantsNotifier()
            
    def WaterPlantsNotifier(self):
        self.log("Notifying Ankith & Sushi to Water plants!")
        self.call_service("notify/mobile_app_iphone_barney", title = "Home plants", message = "Please water all the plants")
        self.call_service("notify/mobile_app_iphone_sushi", title = "Home plants", message = "Please water all the plants")
        self.last_notification = self.now

        