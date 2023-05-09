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
            "show": self.command_show,
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
    def command_show(self, secondary_command):
        """
        'show categories' or 'show category'
        'show week'
        'show month'
        'show overview week'
        'show overview month'
        """
        
        try:
            #--- show categories
            if secondary_command[0] == "categories":
                categories= self.fin_interface.get_categories()
                self.helper.printer("Shwoing all exiting Categories:", color='yellow')
                for category in categories:
                    print(f" - \033[35m{category.get_name()}\033[0m | Budget: {category.get_budget()} EUR ({category.get_type()})")
            
            elif secondary_command[0] == 'week':
                expenses = self.fin_interface.get_week_expenses()
                self.helper.printer("Showing all expenses of the week:", color='yellow')
                for expense in expenses:
                    print(f" - {expense.get_id()}: {expense.get_value()} EUR | {expense.get_name()} (\033[35m{expense.get_category()}\033[0m)")
            
            elif secondary_command[0]== "overview" and secondary_command[1] == 'week':
                self.helper.printer("Showing overview of the week:", color='yellow')
                categories = self.fin_interface.get_categories()
                expenses = self.fin_interface.get_week_expenses()

                expected_maximum = 0
                toal_expenses = 0
                for category in categories:
                    total_category = 0
                    expected_maximum += category.get_budget()
                    #--- Calculate total of the category
                    for expense in expenses:
                        if expense.get_category() == category.get_name():
                            total_category += expense.get_value()
                    
                    #--- Add total expenses
                    toal_expenses += total_category

                    #--- Check to see if it's over budget
                    if total_category > category.get_budget():
                        self.helper.printer(f"[OVER BUDGET] - {category.get_name()}: {total_category} EUR", color='red')
                    else:
                        print(f" - {category.get_name()}: {total_category} EUR | Margin: \033[32m{category.get_budget() - total_category} EUR\033[0m")
                
                #--- Print total expenses
                print("-------------------------------")
                print(f"Total Expenses: {toal_expenses} EUR")
                if toal_expenses > expected_maximum:
                    self.helper.printer(f"[OVER BUDGET] - You are losing: {toal_expenses - expected_maximum} EUR", color='red')

                else:
                    print(f"This week you're saving: \033[32m{expected_maximum - toal_expenses} EUR\033[0m")
                print("-------------------------------")
            else:
                self.helper.printer(f"[ERROR] Command '{secondary_command[0]}' not recognized... Remember to follow the structure: 'show categories' or 'show <week/month>' or 'show overview <week/month>'", color='red')
        
        except IndexError:
            self.helper.printer("[ERROR] Something went wrong... Remember to follow the structure: 'show categories' or 'show <week/month>' or 'show overview <week/month>'", color='red')


    def command_add(self, secondary_command):
        """
        'add <value> in <category> <list(name)>'
        """
        try:
            #--- Extract information from command
            try:
                value = float(secondary_command[0])
            except ValueError:
                self.helper.printer("[ERROR] Value must be a number... Remember to follow the structure: 'add <value> in <category> <(name)>'", color='red')    
                return
            
            category_name = secondary_command[2]
            name = " ".join(secondary_command[3:])

            #--- Get the type of the category
            category = self.fin_interface.get_category(category_name)
            if category is None:
                self.helper.printer(f"[ERROR] Category '{category_name}' does not exist.", color='red')
                return
            
            type = category.get_type()

            #--- Take current time
            datestr = self.helper.get_day_now()

            #--- Create FinEvent object
            fin_event = FinEvent(name=name, value=value, type=type, category=category_name, date=datestr)

            #--- Add FinEvent to database
            self.fin_interface.insert_finance(fin_event)        
        
        except IndexError:
            self.helper.printer("[ERROR] Something went wrong... Remember to follow the structure: 'add <value> in <category> <(name)>'", color='red')

    def command_create(self, secondary_command):
        """
        'create <category> <type> <budget>'
        """
        try:
            #--- Extract information from command
            category = secondary_command[0]
            type = secondary_command[1]
            try:
                budget = int(secondary_command[2])
            except ValueError:
                self.helper.printer("[ERROR] Budget must be a number... Remember to follow the structure: 'create <category> <type> <budget>'", color='red')
                return
            
            #--- Create category in database
            self.fin_interface.insert_category(category, type, budget)
        except IndexError:
            self.helper.printer("[ERROR] Something went wrong... Remember to follow the structure: 'create <category> <type> <budget>'", color='red')

    def command_update(self, secondary_command):
        """
        'update <category> <budget>'
        """
        try:
            #--- Extract information from command
            category = secondary_command[0]
            budget = secondary_command[1]

            #--- check if category exists ---
            category_results = self.fin_interface.get_category(category)
            if category_results is None:
                self.helper.printer(f"[ERROR] Category '{category}' does not exist.", color='red')
                return

            #--- Update category in database
            self.fin_interface.update_category(category, budget)
        except IndexError:
            self.helper.printer("[ERROR] Something went wrong... Remember to follow the structure: 'update <category> <budget>'", color='red')


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


            