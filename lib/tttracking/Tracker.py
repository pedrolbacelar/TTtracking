#--- Import Trackings ---#
from .trackingTT import TTtracker
from .TrackingFin import FinTracker
from .TrackingLearn import LearnTracker 
from .TrackingHabbits import HabbitsTracker

class Tracker():
    def __init__(self, name):
        self.name = name
        self.next_tracking = "task"

    def run(self):
        while True:
            #--- Create the tracking
            if self.next_tracking == "task":
                tracking = TTtracker(f"Task {self.name}")
            elif self.next_tracking == "fin":
                tracking = FinTracker(f"Finan {self.name}")
            elif self.next_tracking == "learn":
                tracking = LearnTracker(f"Learn {self.name}")
            elif self.next_tracking == "myday":
                tracking = HabbitsTracker(f"Myday {self.name}")

            #--- Run the tracking
            self.next_tracking = tracking.run()

