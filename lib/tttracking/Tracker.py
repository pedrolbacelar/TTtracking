#--- Import Trackings ---#
from .trackingTT import TTtracker
from .TrackingFin import FinTracker
from .TrackingLearn import LearnTracker 
from .TrackingHabbits import HabbitsTracker
from .helper import Helper

class Tracker():
    def __init__(self, name):
        self.name = name
        self.next_tracking = "task"
        self.previous_tracking = "task"
        self.flag_run = True
        self.tracking = TTtracker(f"Task {self.name}")
        self.helper = Helper()

    def run(self):
        while True:
            #--- Run the tracking
            if self.flag_run:
                self.previous_tracking = self.next_tracking
                self.next_tracking = self.tracking.run()

            #--- Create the tracking
            if self.next_tracking == "task":
                self.tracking = TTtracker(f"Task {self.name}")
                self.flag_run = True

            elif self.next_tracking == "fin":
                self.tracking = FinTracker(f"Finan {self.name}")
                self.flag_run = True
            
            elif self.next_tracking == "learn":
                self.tracking = LearnTracker(f"Learn {self.name}")
                self.flag_run = True
            
            elif self.next_tracking == "myday":
                self.tracking = HabbitsTracker(f"Myday {self.name}")
                self.flag_run = True
            
            else:
                self.helper.printer(f"[ERROR] '{self.next_tracking}' is not a valid tracking", "red")
                self.next_tracking = self.previous_tracking
                self.flag_run = False    
            

