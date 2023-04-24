from .helper import Helper
helper = Helper()


class Task():
    def __ini__(self, name, tags= None, autostart= None, cluster= None):
        #--- Initialization
        self.name = name
        self.tags = tags
        self.cluster = cluster

        #--- Time star configuration
        if autostart == True:
            (t, tstr) = helper.get_time_now() 
            self.start_timestamp = t
            self.start_string = tstr

        #--- Other Basics
        # End Time
        self.end_timestamp = None
        self.end_string = None

        # Stop Time
        self.stop_timestamp_list = []
        self.start_stop_timestamp = None
        self.end_stop_timestamp = None
        self.total_stopped = 0
        self.flag_stop_time = False

        # Worked Time
        self.worked_time_raw = None
        self.worked_time_clean = None

    def start(self):
        """
        Start the time of the task
        """

        #-- Get current time
        (t, tstr) = helper.get_time_now()
        self.start_timestamp = t
        self.start_string = tstr

        ####################################################
        helper.printer(f"Tasks {self.name} started", 'green')
        ####################################################

    def stop(self):
        """
        Register the time in which the tasks was stopped to subtract in the final end time
        """
        #-- Get current time
        (t,tstr) = helper.get_time_now()
        self.start_stop_timestamp = t
        self.flag_stop_time= True

        ####################################################
        helper.printer(f"Tasks {self.name} stopped", 'red')
        ####################################################
    
    def restart(self):
        """
        Add the end time of the previous stop, add it in stop list, reset stop parameters
        """
        #-- Get current time
        (t, tstr) = helper.get_time_now()
        self.end_stop_timestamp = t

        #--- Interval of stop
        stop_time = self.end_stop_timestamp - self.start_stop_timestamp
        self.stop_timestamp_list.append(stop_time)

        #--- Reset values
        self.start_stop_timestamp = None
        self.end_stop_timestamp = None

        ####################################################
        helper.printer(f"Tasks {self.name} re-started")
        ####################################################

    def finish(self):
        """
        Finish the overall time spent in the task subtracking any stop time
        """

        #-- Get current time
        (t, tstr) = helper.get_time_now()
        self.end_timestamp = t
        self.end_string = tstr

        #-- Stop times
        if self.flag_stop_time:
            for stop in self.stop_timestamp_list:
                self.total_stopped += stop
        
        #-- Delta of working time raw
        self.worked_time_raw = self.end_timestamp - self.start_timestamp
        
        #-- Discounting the stop time (clean worked time)
        self.worked_time_clean = self.worked_time_raw - self.total_stopped

        ####################################################
        helper.printer(f"Tasks {self.name} finished!", 'green')
        helper.printer(f"Raw Time: {self.worked_time_raw}, Clean Time: {self.worked_time_clean}, Stopped Time: {self.stopped_time}")
        ####################################################

    # --------------------- Get Methods ---------------------
    def get_name(self):
        return self.name
    def get_start_time(self):
        return (self.start_timestamp, self.start_string)
    def get_end_time(self):
        return (self.end_timestamp, self.end_string)
    def get_tags(self):
        return self.tags
    def get_worked_time(self):
        return (self.worked_time_clean, self.worke)
    def stopped_time(self):
        return self.total_stopped

class Cluster():
    def __init__(self, name):
        self.name = name

class Tag():
    def __init__(self, name):
        self.name = name
    
    