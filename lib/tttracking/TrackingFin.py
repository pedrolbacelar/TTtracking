from .helper import Helper
from .interfaceDB import interfaceDB
from .components import FinEvent

# TODO:
# - Init
    # - dictionary with all the commands
    # - create object to interface with database
# - Commands
    # - create category
    # - add fin events
    # - update categories budget

class FinTracker():
    def __init__(self, name):
        self.name = name
        self.alive = True
        self.helper = Helper()

        # ------ Dicitionary with all the commands ------
        self.commands = {
            "add": self.command_add,
            "create": self.command_create,
            "update": self.command_update,
            "switch": self.command_switch,
            "kill": self.command_kill
        }

        # ------ Database Management ------
        self.fin_interface = interfaceDB("fin")


    # --------- Main Loop -----------
    def run(self):
        while self.alive:
            #--- Receive command from user
            command = input(f"{self.name}>>> ")

            #--- Parse command into the correct functions
            self.parse_command(command)

        #--- Switch to the next tracking
        return self.next_tracking


    # --------- commands ------------
    def command_add(self, secondary_command):
        """
        'add <value> in <category> <list(name)>'
        """
        #--- Remove firts word
        secondary_command.pop(0)

        #--- Extract information from command
        value = secondary_command[0]
        category_name = secondary_command[2]
        name = " ".join(secondary_command[3:])

        #--- Get the type of the category
        category = self.fin_interface.get_category(category_name)
        type = category[2]

        #--- Take current time
        datestr = self.helper.get_day_now()

        #--- Create FinEvent object
        fin_event = FinEvent(name=name, value=value, type=type, category=category_name, date=datestr)

        #--- Add FinEvent to database
        self.fin_interface.insert_finance(fin_event)        
        
    def command_create(self, secondary_command):
        """
        'create <category> <type> <budget>'
        """
        #--- Remove firts word
        secondary_command.pop(0)

        #--- Extract information from command
        category = secondary_command[0]
        type = secondary_command[1]
        budget = secondary_command[2]

        #--- Create category in database
        self.fin_interface.insert_category(category, type, budget)


    def command_update(self, secondary_command):
        """
        'update <category> <budget>'
        """
        #--- Remove firts word
        secondary_command.pop(0)

        #--- Extract information from command
        category = secondary_command[0]
        budget = secondary_command[1]

        #--- Update category in database
        self.fin_interface.update_category(category, budget)

    def command_switch(self, secondary_command):
        """
        switch task
        switch fin
        switch daily
        """
        
        #--- Take the name of swicthing tracking
        self.next_tracking = secondary_command[0]
        
        #--- Kill the condition of the main loop
        self.alive = False

        self.helper.printer(f" --- Swtiching to Tracking '{self.next_tracking}' ---", 'brown')

    def command_kill(self, secondary_command):
        self.helper.kill(self.name)


    # --------- Helping Functions ------------
    def parse_command(self, command):
        args = command.split()
        if args[0] in self.commands:
            secondary_command = args[1:]
            self.commands[args[0]](secondary_command)
        else:
            self.helper.printer(f"[ERROR] Command {command} not found", color='red')