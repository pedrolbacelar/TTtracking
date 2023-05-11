"""
------Description of this tracking service: ------
- Itens to track my daily habbits
- Use every day before sleeping
- When activate, ask for some comments of the day
- Than ask for the habbits

------ Features: ------
- Add new days and track the habbits ofr that day
- Create new Habbits
- Show existing habbits
- Track performance (Future)

------ Database structure: ------
Habbits_table [id, name, status, comment, day]
Days_table [id, comment, day]

------ Commands: ------
- Create habbit <name>
- myday <comment> # comments of the day
    - <habbit> <comment> # comments of the habbit

- Show habbits
- Show habbit <name>
- Show days
- Show day <id>

------ Objects structure: ------
Habbit object:
- name
- status (True or False) : The habbit was fulfilled or not
- comment
- id

Day object:
- comment
- id

------ Examples: ------
>>> Create habbit meditation
>>> myday Today was good day, we deliver a good presentation
--- > meditation: ""
        > comment: It was good to meditate
--- > sleep: "f"
--- > exercise: ""
        > comment: ""

"""
from .helper import Helper
from .interfaceDB import interfaceDB
from .components import Habbit, Day

class HabbitsTracker():
    def __init__(self, name):
        self.helper = Helper()
        self.name = name
        self.next_tracking = "habbits"
        self.alive = True

        #--- Dictionary of commands ---#
        self.commands = {
            "create": self.command_create_habbit,
            "myday": self.command_myday,
            "show": self.command_show,
            "help": self.command_help,
            "switch": self.command_switch,
            "kill": self.command_kill,
        }

        #--- Database Management ---#
        self.habbit_interface = interfaceDB("habbit")
    
    # ------- Main Loop -------
    def run(self):
        while self.alive:
            #--- Receive command from user
            command = input(f"{self.name}>>> ")

            #--- Parse command into the correct functions
            self.parse_command(command)

        #--- Switch to the next tracking
        return self.next_tracking
    
    # ------- Commands -------

    def command_help(self, secondary_command):
        self.helper.printer("Helping you!")
        print("|--- \033[33mcreate\033[0m <habbit_name>")
        print("|--- \033[33mmyday\033[0m <comment>")
        print("|--- \033[33mshow\033[0m habbits")
        print("|--- \033[33mshow\033[0m habbit <name>")
        print("|--- \033[33mshow\033[0m days")
        print("|--- \033[33mshow\033[0m day <id>")
        print("|--- \033[33mswitch\033[0m <tracking>")
        print("|--- \033[33mkill\033[0m")

        
    
    def command_create_habbit(self, secondary_command):
        """
        create habbit <name>
        """
        #--- Take the name of the habbit
        habbit_name = secondary_command[0]

        #--- Create the habbit object
        habbit = Habbit(name=habbit_name)

        #--- Insert it into the database
        self.habbit_interface.insert_habbit(habbit)

        #--- Create the habbit
        self.helper.printer(f"---- Creating habbit '{habbit_name}' ----", 'brown')

    def command_myday(self, secondary_command):
        """
        myday <comment>
        """
        #--- Take the comment of the day
        comment = " ".join(secondary_command)

        #--- Create the day object
        day = Day(comment=comment)

        #--- Insert it into the database
        self.habbit_interface.insert_day(day)

        #-------- Check Habbits for that day --------#
        #--- Get all the habbits
        habbits_names = self.habbit_interface.get_unique_habbits_names()

        #--- Ask for the status of each habbit
        for habbit_name in habbits_names:
            status = input(f"{habbit_name} status >>> ")
            comment = input(f"\033[33m{habbit_name} comment >>>\033[0m ")

            #--- Create the habbit object
            habbit = Habbit(name=habbit_name, status=status, comment=comment)

            #--- Insert it into the database
            self.habbit_interface.insert_habbit(habbit)

    def command_show(self, secondary_command):
        """
        show habbits
        show habbit <name>
        show days
        """
        if len(secondary_command)== 0  or secondary_command[0] == "habbits":
            #--- Get all the habbits
            habbits = self.habbit_interface.show_all_habbits()
            self.helper.printer(f"---- Showing all habbits ----")
            #--- Print the cards
            print("   HABBIT IDs   |   HABBIT NAME")

            #--- Print each habbit
            for habbit in habbits:
                habbit_id = habbit.get_id()
                habbit_name = habbit.get_name()
                habbit_comment = habbit.get_comment()
                habbit_status = habbit.get_status()
                habbit_date = habbit.get_day()

                if habbit_id < 10:
                    print(f"       {habbit_id}        |   \033[35m{habbit_date} ,{habbit_name}\033[0m - \033[33m{habbit_status}\033[0m - {habbit_comment}")
                elif habbit_id > 9 and habbit_id < 100:
                    print(f"      {habbit_id}        |   \033[35m{habbit_date} ,{habbit_name}\033[0m - \033[33m{habbit_status}\033[0m - {habbit_comment}")
                elif habbit_id > 99:
                    print(f"     {habbit_id}        |   \033[35m{habbit_date} ,{habbit_name}\033[0m - \033[33m{habbit_status}\033[0m - {habbit_comment}")

        elif secondary_command[0] == "habbit":
            #--- Get the habbit name
            habbit_name = secondary_command[1]

            #--- Get the habbit
            habbits = self.habbit_interface.show_from_habbit(habbit_name)

            #--- Print the cards
            print("   HABBIT IDs   |   HABBIT NAME")


            #--- Print each habbit
            for habbit in habbits:
                habbit_id = habbit.get_id()
                habbit_name = habbit.get_name()
                habbit_comment = habbit.get_comment()
                habbit_status = habbit.get_status()
                habbit_date = habbit.get_day()

                if habbit_id < 10:
                    print(f"       {habbit_id}        |   \033[35m{habbit_date} ,{habbit_name}\033[0m - \033[33m{habbit_status}\033[0m - {habbit_comment}")
                elif habbit_id > 9 and habbit_id < 100:
                    print(f"      {habbit_id}        |   \033[35m{habbit_date} ,{habbit_name}\033[0m - \033[33m{habbit_status}\033[0m - {habbit_comment}")
                elif habbit_id > 99:
                    print(f"     {habbit_id}        |   \033[35m{habbit_date} ,{habbit_name}\033[0m - \033[33m{habbit_status}\033[0m - {habbit_comment}")

        
        
        
        elif secondary_command[0] == "days":
            #--- Get all the days
            days = self.habbit_interface.show_days()

            
            #--- Print the cards
            self.helper.printer("Showing all open cards:")
            print("   HABBIT IDs   |   HABBIT NAME")

            
            #--- Print each habbit
            for day in days:
                day_id = day.get_id()
                day_comment = day.get_comment()
                day_date = day.get_day()

                if day_id < 10:
                    print(f"       {day_id}        |   \033[35m{day_date}\033[0m - {day_comment}")
                elif day_id > 9 and day_id < 100:
                    print(f"      {day_id}        |   \033[35m{day_date}\033[0m - {day_comment}")
                elif day_id > 99:
                    print(f"     {day_id}        |   \033[35m{day_date}\033[0m - {day_comment}")





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

        self.helper.printer(f"---- Swtiching to Tracking '{self.next_tracking}' ----", 'brown')

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



