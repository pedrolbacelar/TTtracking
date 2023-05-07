#--- Import Trackings ---#
from .trackingTT import TTtracker
from .TrackingFin import FinTracker

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

            #--- Run the tracking
            self.next_tracking = tracking.run()

