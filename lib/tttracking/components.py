from .helper import Helper
helper = Helper()


class Task():
    def __init__(self, name, id, tags= None, autostart= None, cluster= None):
        #--- Initialization
        self.helper = Helper()
        self.name = name
        self.id = id
        self.tags = tags
        self.cluster = cluster
        self.start_timestamp= None

        #--- Time star configuration
        if autostart == True:
            (tstr, t) = helper.get_time_now() 
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
        (tstr, t) = helper.get_time_now()
        self.start_timestamp = t
        self.start_string = tstr

        ####################################################
        helper.printer(f"Task '{self.name}' started", color='green', time= True)
        ####################################################

    def stop(self):
        """
        Register the time in which the tasks was stopped to subtract in the final end time
        """
        #-- Get current time
        (tstr,t) = helper.get_time_now()
        self.start_stop_timestamp = t
        self.flag_stop_time= True

        ####################################################
        helper.printer(f"Task '{self.name}' stopped", color='red', time= True)
        ####################################################
    
    def restart(self):
        """
        Add the end time of the previous stop, add it in stop list, reset stop parameters
        """
        #-- Get current time
        (tstr, t) = helper.get_time_now()
        self.end_stop_timestamp = t

        #--- Interval of stop
        stop_time = self.end_stop_timestamp - self.start_stop_timestamp
        self.stop_timestamp_list.append(stop_time)

        #--- Reset values
        self.start_stop_timestamp = None
        self.end_stop_timestamp = None

        ####################################################
        helper.printer(f"Task '{self.name}' re-started", time= True)
        ####################################################

    def finish(self):
        """
        Finish the overall time spent in the task subtracking any stop time
        """

        #-- Get current time
        (tstr, t) = helper.get_time_now()
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
        helper.printer(f"Task '{self.name}' done!", color='green', time= True)
        helper.printer(f"Raw Time: {self.helper.sec2min(self.worked_time_raw)} min, Clean Time: {self.helper.sec2min(self.worked_time_clean)} min, Stopped Time: {self.helper.sec2min(self.total_stopped)} min")
        ####################################################

    # --------------------- Get Methods ---------------------
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_start_timestamp(self):
        return self.start_timestamp
    def get_start_string(self):
        return self.start_string
    def get_end_timestamp(self):
        return self.end_timestamp
    def get_end_string(self):
        return self.end_string
    def get_tags(self):
        return self.tags
    def get_cluster(self):
        return self.cluster
    def get_worked_time_clean(self):
        return self.worked_time_clean
    def get_worked_time_raw(self):
        return self.worked_time_raw
    def get_stopped_time(self):
        return self.total_stopped


    # ------------------------ SET METHODS ------------------------
    def set_worked_clean(self, clean_tme):
        self.worked_time_clean = clean_tme
    def set_manual_edited(self):
        (tsrt, t) = self.helper.get_time_now()
        self.start_string = f"edited - {tsrt}"
        self.end_string = f"edited - {tsrt}"

class FinEvent():
    def __init__(self, name, category, type, value, date):
        self.name = name
        self.category = category
        self.value = value
        self.date = date
        self.type = type

    
    # --------------------- Get Methods ---------------------
    def get_name(self):
        return self.name
    def get_category(self):
        return self.category
    def get_value(self):
        return self.value
    def get_date(self):
        return self.date
    
    