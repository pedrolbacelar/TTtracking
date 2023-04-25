from .interfaceDB import interfaceDB
from .components import Task
from .components import Tag
from .components import Cluster
from .helper import Helper

class TTtracker():
    def __init__(self,name):
        self.helper = Helper()
        self.name = name
        self.condition = True
        self.current_tasks = []

        # ----- Database Management -----
        self.task_interfaceDB = interfaceDB("task")


        # ----- COMMANDS DICTIONARY -----
        self.commands_store = {
            "add":  self.commmand_create_task,
            "show": self.command_show_task,
            "start": self.command_start_task,
            "stop": self.command_stop_task,
            "restart": self.command_restart_task,
            "finish": self.command_finish_task,
            "help": self.command_help,
            "kill": self.command_kill
        }


    def run(self):
        # ------ Infinity Loop ------
        while self.condition:
            #--- Receives the Input 
            command = input(f"{self.name}>> ")

            #--- Extracts the words
            (main_command, secondary_command) = self.extractor(command)

            #--- Assign the right function
            try:
                self.commands_store[main_command](secondary_command)
            except KeyError:
                self.helper.printer(f"------ [ERROR] '{main_command}' is not an available command! ------", 'red')
                self.commands_store["help"](secondary_command)


    # ===================== HELPING FUNCTIONS =====================
    
    def extractor(self, command):
        """
        Extract all the words of the command phrase
        """
        words_extracted = command.split()

        #--- Segmentation
        main_command = words_extracted[0]
        secondary_command = words_extracted[1:]
        
        return (main_command, secondary_command)

    # ===================== COMMANDS FUNCTIONS =====================

    def command_help(self, secondary_command):
        self.helper.printer("Available Commands:")
        print("|--- add     - Create a new tasks (e.g, 'add my new task')")
        print("|--- show    - Show tasks without a Start (e.g, 'show')")
        print("|--- start   - Start the most recent task created or a specific task (e.g, 'start', 'start 1')")
        print("|--- stop    - Stop the most recent task created or a specific task (e.g, 'stop', 'stop 1')")
        print("|--- restart - Restart the most recent task created or a specific task (e.g, 'restart', 'restart 1')")
        print("|--- finish  - Finish the most recent task created or a specific task (e.g, 'finish', 'finish 1')")
        print("|--- kill    - Kill the application (e.g, 'kill')")

    def commmand_create_task(self, secondary_command):
        """
        Create a task based on the secondary command and add it into the database

        secondary_command: list of string
        """
        #--- Create a task object
        name = " ".join(secondary_command)

        #--- Get the next task id
        id= self.task_interfaceDB.get_next_taks_id()

        #--- Create Task
        new_task = Task(name= name, id= id)

        #--- Insert it into the database
        self.task_interfaceDB.insert_task(new_task)

        #--- Add task the working tasks
        self.current_tasks.append(new_task)


    def command_show_task(self, secondary_command):
        """
        Show all the tasks that don't have a start_time
        """
        #--- Get open tasks
        open_tasks = self.task_interfaceDB.get_open_tasks()
        
        self.helper.printer("Showing all open tasks:")
        print("   TASKS IDs   |   TASK NAME")
        for taks in open_tasks:
            print(f"       {taks[0]}       |   {taks[1]}")

    def command_start_task(self,secondary_command):
        """
        From the secondary command the function identify the task ID,
        create the task object and start the clock for it

        command:
        "start 1"
        "start 3"

        TODO:
        1) Extract the task id
        2) Get the tasks property from the database
        3) Create a tasks object
        4) Add it into the working tasks
        5) Start the clock
        """

        if len(secondary_command) != 0: 
            #--- Get task ID
            id = int(secondary_command[0])

            #--- Get the tasks property from the database
            task_property = self.task_interfaceDB.get_property(id)

            #--- Create task object
            new_task = Task(
                name= task_property[1],
                id= id,
                tags= task_property[4],
                cluster= task_property[5]
            )

            #--- Start clock
            new_task.start()

            #--- Add the current tasks
            self.current_tasks.append(new_task)

            #--- Update database
            self.task_interfaceDB.update_task(new_task)
        
        else:
            #--- Get the most recent task
            current_task = self.current_tasks[-1]

            #--- Start clock
            current_task.start()

            #--- Update database
            self.task_interfaceDB.update_task(current_task)

    def command_stop_task(self, secondary_command):
        """
        Stop the most recent tasks of the current task if 
        secondary is empty or stop a specific task id if 
        it is not.

        command:
        "stop"
        "stop 3"

        TODO:
        1) Extract the ID of the secondary command
        2) If id is empty:
            3) Get the recent task object 
            4) Stop the tasks
        5) else:
            6) From all the current tasks, get the one if the rigth ID
            7) Stop the task
        """

        #--- Secondary Tasks Empty
        if len(secondary_command) == 0:
            #--- Get the current task
            current_task = self.current_tasks[-1]

            #--- Stop the task
            current_task.stop()

        else:
            task_id = int(secondary_command[0])

            for current_task in self.current_tasks:
                if current_task.get_id() == task_id:
                    current_task.stop()

        #--- Update database
        self.task_interfaceDB.update_task(current_task)

    def command_restart_task(self, secondary_command):
        #--- Secondary Tasks Empty
        if len(secondary_command) == 0:
            #--- Get the current task
            current_task = self.current_tasks[-1]

            #--- Restart the task
            current_task.restart()

        else:
            task_id = int(secondary_command[0])

            for current_task in self.current_tasks:
                if current_task.get_id() == task_id:
                    current_task.restart()

        #--- Update database
        self.task_interfaceDB.update_task(current_task)

    def command_finish_task(self, secondary_command):
        #--- Secondary Tasks Empty
        if len(secondary_command) == 0:
            #--- Get the current task
            current_task = self.current_tasks[-1]

            #--- Finish the task
            current_task.finish()

        else:
            task_id = int(secondary_command[0])

            for current_task in self.current_tasks:
                if current_task.get_id() == task_id:
                    current_task.finish()

        #--- Update database
        self.task_interfaceDB.update_task(current_task)

    def command_kill(self, secondary_command):
        self.helper.kill(self.name)

    
