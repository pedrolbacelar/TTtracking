from IPython.display import Markdown, display
from playsound import playsound
import os

#--- Common Libraries
import datetime
from datetime import datetime as dtime

import calendar
from time import sleep
import shutil
import os
import re
import sys
import json




class Helper():
    def __init__(self, type= "py"):
        self.type = type

        #--- Get global path of the library
        # Get the directory of the code.py file
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        #--- To print on the normal terminal
        if self.type == "py":
            self.Red= "\033[31m"
            self.Green= "\033[32m"
            self.Yellow= "\033[33m"
            self.Blue= "\033[34m"
            self.Purple= "\033[35m "
            self.Brown= "\033[38;5;94m "
            self.Reset = '\033[0m'

        #--- To print on the Jupyter Notebook
        else:
            self.Red = "<span style='color:red'>"
            #self.Green = "<span style='color:green'>"
            self.Green = "<span style='color:#7DCEA0'>"
            self.Yellow = "<span style='color:yellow'>"
            self.Blue = "<span style='color:#3498DB'>"
            self.Purple = "<span style='color:#A569BD'>"
            self.Brown = "<span style='color:#DC7633'>"
            self.Reset = "</span>"

        self.colors = {
            'red': self.Red,
            'green': self.Green,
            'yellow': self.Yellow,
            'blue': self.Blue,    
            'purple': self.Purple,
            'brown': self.Brown,
            'reset': self.Reset                 
            }

        #--- Construct the sounds paths
        self.sounds = {
            'red': os.path.join(self.dir_path, 'sound', 'error.mp3'),
            'green': os.path.join(self.dir_path, 'sound', 'success.mp3'),
            'yellow': os.path.join(self.dir_path, 'sound', 'warning.mp3'),
            'clock': os.path.join(self.dir_path, 'sound', 'clock alarm.mp3'),
            'tick': os.path.join(self.dir_path, 'sound', 'tick tack.mp3'),
            'sirene': os.path.join(self.dir_path, 'sound', 'sirene alert.mp3'), 
        }
    
    #--- Printing with colors
    def printer(self, text, color= 'yellow', time= False, play= True):
        (tstr, t) = self.get_time_now()
        if time == True:
            if self.type == "py":
                print(f"{self.colors[color]}{tstr} | {text}{self.Reset}")
            
            else:
                display(Markdown(f"{self.colors[color]}{tstr} | {text}{self.Reset}"))
        else:
            if self.type == "py":
                print(f"{self.colors[color]}{text}{self.Reset}")
            
            else:
                display(Markdown(f"{self.colors[color]}{text}{self.Reset}"))

    def play(self, sound= 'tick'):
        try:
            playsound(self.sounds[sound])
        except KeyError:
            self.printer(f"Sound {sound} not found", color= 'red')
            print("Available sounds: ")
            for key in self.sounds.keys():
                print(f" - {key}")

    #--- Get all the internal colors
    def get_colors(self):
        return self.colors
    
    #--- Get the timestemp and translate it
    def get_time_now(self, verbose= False):
        current_timestamp = datetime.datetime.now().timestamp()
        current_timestamp = round(current_timestamp)
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%d %B %Y %H:%M:%S")

        if verbose == True:
            print(f"Current Time: {current_time_str}")
            print(f"Current Timestamp: {current_timestamp}")

        return (current_time_str, current_timestamp)
    
    def get_day_now(self):
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%d %B %Y")
        return current_time_str
    
    def get_day_timestamp(self, date_str= None):
        if date_str == None:
            date_str = self.get_day_now()

        date = datetime.datetime.strptime(date_str, "%d %B %Y")
        return int(date.timestamp())
    def get_timestamp(self, time):
        date = datetime.datetime.strptime(time, "%Y-%B-%d %H:%M:%S")
        return int(date.timestamp())
    
    def convert_timestamp_to_date(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime("%d %B %Y")
    
    def get_current_day(self):
        """
        Returns the current day in the format "%d %B %Y".

        Returns:
            str: The current day in the format "%d %B %Y".
        """
        current_date = dtime.now().strftime("%d %B %Y")
        return current_date 

    def get_current_and_previous_day(self):
        """
        Returns the current day and the previous day in the format "%d %B %Y".

        Returns:
            str: The current day and the previous day in the format "%d %B %Y".
        """
        current_date = (dtime.now() + datetime.timedelta(days=1)).strftime("%d %B %Y")
        previous_date = (dtime.now() - datetime.timedelta(days=1)).strftime("%d %B %Y")
        return current_date, previous_date
    
    def convert_date_string(self, date_str):
        """
        Converts a date string in the format of "%Y-%B-%d %H:%M:%S" to "%d %B %Y".

        Args:
            date_str (str): The date string in the format of "%Y-%B-%d %H:%M:%S".

        Returns:
            str: The date string in the format of "%d %B %Y".
        """
        date_obj = dtime.strptime(date_str, "%Y-%B-%d %H:%M:%S")
        return date_obj.strftime("%d %B %Y")
    
    def convert_SQL_date(self,date):
        parsed_date = dtime.strptime(date, "%d %B %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date
    
    def convert_daystr_to_timestamp(self, date_str):
        """
        Takes the date string in the format of "%d %B %Y %H:%M:%S" and returns the timestamp.
        """

        date_obj = dtime.strptime(date_str, "%d %B %Y %H:%M:%S")
        return int(date_obj.timestamp())
    
    def convery_day_to_timestamp(self, date_str):
        """
        Takes the date string in the format of "%d %B %Y" and returns the timestamp.
        """
        date_obj = dtime.strptime(date_str, "%d %B %Y")
        return int(date_obj.timestamp())

    # --- create a function that takes the current day and give
    # back the first day and last day of the week, considering that
    # the week starts on Monday and finishes on Sunday
    def get_week(self, date_str = None):
        "2023-05-08 00:00:00 2023-05-14 00:00:00"
        if date_str == None:
            date_str = self.get_current_day()
        date = datetime.datetime.strptime(date_str, "%d %B %Y")
        day = date.weekday()
        if day == 0:
            first_day = date
        else:
            first_day = date - datetime.timedelta(days=day)
        last_day = first_day + datetime.timedelta(days=6)

        #--- Convert to default day string format
        first_day = self.convert_date_string(first_day.strftime("%Y-%B-%d %H:%M:%S"))
        last_day = self.convert_date_string(last_day.strftime("%Y-%B-%d %H:%M:%S"))

        return (first_day, last_day)
    
    def get_month(self, date_str= None):
        "2023-04-01 00:00:00 2023-04-30 00:00:00"
        if date_str == None:
            date_str = self.get_current_day()
        date = datetime.datetime.strptime(date_str, "%d %B %Y")
        first_day = date.replace(day=1)
        last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
        
        #--- Convert to default day string format
        first_day = self.convert_date_string(first_day)
        last_day = self.convert_date_string(last_day)
        
        return (first_day, last_day)


    #--- Copy one file into a new path
    def duplicate_file(self, reference_file, copied_file):
        shutil.copy2(reference_file, copied_file)
    
    #--- Create a file base on the path
    def create_file(self, file_path):
        # If folder doesn't exist, creates folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    #--- Extract the first number in a string
    def extract_int(self, string):
        integer = int(re.findall('\d+', string)[0])
        return integer
    
    def kill(self, name):
        #--- Killing the program
        self.printer(f"---- {name} killed ----", 'red')
        sys.exit()

    def convert_stringVect_to_listVect(self, stringVect):
        return json.loads(stringVect)
    
    def convert_tuple_vector_to_list(self, tuple_vector):
        for i in range(len(tuple_vector)):
            tuple_vector[i] = tuple_vector[i][0]
        return tuple_vector
    
    def convert_list_to_string(self, lists):
        string = " ".join(lists)
        return string
    
    def sec2min(self, sec):
        return round(sec/60)
    def mind2sec(self, min):
        return min*60
    def sec2hour(self,sec):
        return round(sec/3600)