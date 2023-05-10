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
    def __init__(self, name, category, type, value, date, id= None):
        self.name = name
        self.category = category
        self.value = value
        self.date = date
        self.type = type
        self.id = id

    
    # --------------------- Get Methods ---------------------
    def get_name(self):
        return self.name
    def get_category(self):
        return self.category
    def get_value(self):
        return self.value
    def get_date(self):
        return self.date
    def get_type(self):
        return self.type
    def get_id(self):
        return self.id

class FinCategory():
    def __init__(self, name, type, budget, id= None):
        self.name = name
        self.type = type
        self.budget = budget
        self.id = id
    
    # --------------------- Get Methods ---------------------
    def get_name(self):
        return self.name
    def get_type(self):
        return self.type
    def get_budget(self):
        return int(self.budget)
    def get_id(self):
        return self.id

class Card():
    # CARD CLASS STRUCTURE:
    # - Card: [id, front, back, type, last_review, next_review, interval, nreviews, nfailed]
    # update_review(success= True): 
    #   if success == True:
    #       update card after correct answer - interval = interval * 2 (update next_review)
    #   if success == False:
    #       update card after failed answer -  interval = 1 (update next_review)

    def __init__(self, front, back, last_review= None, next_review= None, type= "new", interval= 1, nreviews= 0, nfailed= 0, id= None):
        self.helper = Helper()

        #--- Card Basic Informations
        self.id = id
        self.front = front
        self.back = back
        self.interval = interval
        self.nreviews = nreviews
        self.nfailed = nfailed
        self.type = type

        #--- Next Review
        if next_review == None:
            self.next_review = self.helper.get_day_now()
        else:
            self.next_review = next_review

        #--- Last Review
        if last_review == None:
            self.last_review = self.helper.get_day_now()
        else:
            self.last_review = last_review
    
    # --------------------- Update Methods ---------------------
    def update_review(self, success= True):
        #--- Update last review
        self.last_review = self.helper.get_day_now()

        #--- Update card settings
        if success:
            if self.interval == 0:
                self.interval = 1
            self.interval *= 2
            self.nreviews += 1
            self.type = "learning"
        else:
            self.interval = 0
            self.nfailed += 1
            self.type = "failed"

        #--- Update next review (integer)
        self.next_review = self.helper.get_day_timestamp() + self.interval * 86400

        #--- Convert timestamp (integer) to day string
        self.next_review = self.helper.convert_timestamp_to_date(self.next_review)

        return self.next_review

    # --------------------- Get Methods ---------------------
    def get_id(self):
        return self.id
    def get_front(self):
        return self.front
    def get_back(self):
        return self.back
    def get_last_review(self):
        return self.last_review
    def get_next_review(self):
        return self.next_review
    def get_interval(self):
        return self.interval
    def get_nreviews(self):
        return self.nreviews
    def get_nfailed(self):
        return self.nfailed
    def get_type(self):
        return self.type

"""
------ Objects structure: ------
Habbit object:
- name
- status (True or False) : The habbit was fulfilled or not
- comment
- id

Day object:
- comment
- id
"""

class Habbit():
    def __init__(self, name, status= None, comment= None, id= None, day= None):
        self.helper = Helper()
        self.name = name
        self.status = status
        self.comment = comment
        self.id = id
        if day == None:
            self.day = self.helper.get_day_now()
        else:
            self.day = day
    
    # --------------------- Get Methods ---------------------
    def get_name(self):
        return self.name
    def get_status(self):
        return self.status
    def get_comment(self):
        return self.comment
    def get_id(self):
        return self.id
    def get_day(self):
        return self.day

class Day():
    def __init__(self, comment= None, id= None, day= None):
        self.helper = Helper()
        self.comment = comment
        self.id = id
        if day == None:
            self.day = self.helper.get_day_now()
        else:
            self.day = day

    
    # --------------------- Get Methods ---------------------
    def get_comment(self):
        return self.comment
    def get_id(self):
        return self.id
    def get_day(self):
        return self.day
    