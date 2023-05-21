from .interfaceDB import interfaceDB
from .components import Task
from .plotter import Plotter
from .helper import Helper

class TTtracker():
    def __init__(self,name):
        self.helper = Helper()
        self.name = name
        self.alive = True
        self.next_tracking = "task"
        self.current_tasks = []
        self.working_task = None
        self.cluster_adding = None

        self.plotter = Plotter("Plotter")
        # ----- Database Management -----
        self.task_interfaceDB = interfaceDB("task")
        self.cluster_interfaceDB = interfaceDB("cluster")
        self.myday_interfaceDB = interfaceDB("myday")

        # ----- COMMANDS DICTIONARY -----
        self.commands_store = {
            "add":  self.commmand_create_task,
            "show": self.command_show_task,
            "start": self.command_start_task,
            "stop": self.command_stop_task,
            "restart": self.command_restart_task,
            "finish": self.command_finish_task,
            "create": self.command_create,
            "myday": self.command_myday,
            "switch": self.command_switch,
            "set": self.command_set,
            "plot": self.command_plot,
            "help": self.command_help,
            "kill": self.command_kill
        }


    def run(self):
        # ------ Infinity Loop ------
        while self.alive:
            #--- Receives the Input 
            command = input(f"{self.name}>>> ")

            #--- Extracts the words
            (main_command, secondary_command) = self.extractor(command)

            #--- Assign the right function
            try:
                self.commands_store[main_command](secondary_command)
            except KeyError:
                self.helper.printer(f"------ [ERROR] '{main_command}' is not an available command! ------", 'red')
                self.commands_store["help"](secondary_command)

        #--- Just to confirm
        if self.alive == False:
            return self.next_tracking
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
        # ----- Choosing Cluster -----
        #--- Task with a cluster
        if secondary_command[0] == 'in':
            secondary_command.pop(0)
            self.cluster_adding = secondary_command.pop(0)


        #--- check cluster existing ---
        if self.check_clusters(self.cluster_adding):

            #--- Create a task object
            name = " ".join(secondary_command)
            cluster_name = self.cluster_adding

            

            #--- Get the next task id
            id= self.task_interfaceDB.get_next_taks_id()

            #--- Create Task
            new_task = Task(name= name, id= id, cluster= cluster_name)

            #--- Insert it into the database
            self.task_interfaceDB.insert_task(new_task)

            #--- Add task the working tasks
            self.current_tasks.append(new_task)

    def command_show_task(self, secondary_command):
        """
        'show': Show all the tasks that don't have a start_time
        'show clusters': Show all created clusters
        'shows cluster_name': Show all tasks created with the cluster cluster_name
        """
        
        # --- No secondary command
        if len(secondary_command) == 0:
            #--- Get open tasks
            open_tasks = self.task_interfaceDB.get_open_tasks()
            
            self.helper.printer("Showing all open tasks:")
            print("   TASKS IDs   |   TASK NAME")
            for taks in open_tasks:
                if taks[0] < 10:
                    print(f"       {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
                elif taks[0] > 9 and taks[0] < 100:
                    print(f"      {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
                elif taks[0] > 99:
                        print(f"     {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")

        # --- Showing existing cluster
        elif secondary_command[0] == "clusters" or secondary_command[0] == "cluster":
            #--- Get clusters IDs and Names from the database
            clusters = self.cluster_interfaceDB.get_clusters()
            
            #--- Interface
            self.helper.printer("Showing all clusters:")
            print("   CLUSTER ID  |   CLUSTER NAME")
            for cluster in clusters:
                if cluster[0] < 10:
                    print(f"       {cluster[0]}       |   {cluster[1]}")
                elif cluster[0] > 10:
                    print(f"      {cluster[0]}       |   {cluster[1]}")

        # --- Showing tasking from a specific cluster
        elif secondary_command[0] == "from":
            #--- get cluster name
            cluster_name = secondary_command[1]
            
            #--- Check to see the cluster exists
            if self.check_clusters(cluster_name):

                #--- Get tasks from specific cluster
                open_tasks = self.task_interfaceDB.get_tasks_from_cluster(cluster_name)
                
                self.helper.printer(f"Showing all open tasks FROM {cluster_name}:")
                print("   TASKS IDs   |   TASK NAME")
                for taks in open_tasks:
                    if taks[0] < 10:
                        print(f"       {taks[0]}       |   {taks[1]}")
                    elif taks[0] > 9 and taks[0] < 100:
                        print(f"      {taks[0]}       |   {taks[1]}")
                    elif taks[0] > 99:
                        print(f"     {taks[0]}       |   {taks[1]}")

        elif secondary_command[0] == "working":
            if self.working_task != None:
                if self.working_task.get_end_string() == None:
                    self.helper.printer(f"You are working on this task at the moment: '{self.working_task.get_name()}' and Started at: {self.working_task.get_start_string()}", time= True)
                else:
                    self.helper.printer(f"You are not working in any task, the last one was: '{self.working_task.get_name()}' and Finished at {self.working_task.get_end_string()}")
                    
            else:
                self.helper.printer("You didn't started any task within this scope")
        
        elif secondary_command[0] == "myday":
            #--- Get open tasks
            open_tasks = self.myday_interfaceDB.get_open_myday()
            
            self.helper.printer("Showing all open day tasks:")
            print("   TASKS IDs   |   TASK NAME")
            for taks in open_tasks:
                if taks[0] < 10:
                    print(f"       {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
                elif taks[0] > 9 and taks[0] < 100:
                    print(f"      {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
                elif taks[0] > 99:
                    print(f"     {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
        
        elif secondary_command[0] == "idle":
            """
            show idle: shows the tasks started but not finished
            for helping setting it correctly when the user
            forget to finished it
            """

            idle_tasks = self.task_interfaceDB.get_idle_tasks()
            if len(idle_tasks) > 0:
                self.helper.printer("Showing all idle tasks:")
                print("   TASKS IDs   |   TASK NAME")
                for taks in idle_tasks:
                    if taks[0] < 10:
                        print(f"       {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
                    elif taks[0] > 9 and taks[0] < 100:
                        print(f"      {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")
                    elif taks[0] > 99:
                            print(f"     {taks[0]}       |   \033[35m{taks[2]}\033[0m - {taks[1]}")

            else:
                self.helper.printer(f"[WARNING] No idle tasks found, i.e., no tasks with started and without an end time", 'brown')

        #--- If it's nothing raise a message
        else:
            self.helper.printer(f"[ERROR] The sub-command '{secondary_command[0]}' is not valid.", 'red')
            self.helper.printer(f"Available sub-command to mix with 'show':")
            print("|--- 'show clusters': show all available clusters")
            print("|--- 'show from cluster_X': Show open task from cluster_X")

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
            task = Task(
                name= task_property[1],
                id= id,
                tags= task_property[4],
                cluster= task_property[5]
            )

            #--- Start clock
            task.start()

            #--- Add the current tasks
            self.current_tasks.append(task)

            #--- Update database
            self.task_interfaceDB.update_task(task)
        
        else:
            #--- Get the most recent task
            task = self.current_tasks[-1]

            #--- Start clock
            task.start()

            #--- Update database
            self.task_interfaceDB.update_task(task)

        #--- Update position in current task
        self.update_positioning(task.get_id())

        #--- Update the current working task
        self.working_task = task

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
            #--- Stop the task
            self.working_task.stop()

            #--- Update database
            self.task_interfaceDB.update_task(self.working_task)

        else:
            task_id = int(secondary_command[0])

            for current_task in self.current_tasks:
                if current_task.get_id() == task_id:
                    current_task.stop()

            #--- Update position in current task
            self.update_positioning(current_task.get_id())

            #--- Update database
            self.task_interfaceDB.update_task(current_task)

    def command_restart_task(self, secondary_command):
        #--- Secondary Tasks Empty
        if len(secondary_command) == 0:
            #--- Restart the task
            self.working_task.restart()

            #--- Update database
            self.task_interfaceDB.update_task(self.working_task)            

        else:
            task_id = int(secondary_command[0])

            for current_task in self.current_tasks:
                if current_task.get_id() == task_id:
                    current_task.restart()

            #--- Update database
            self.task_interfaceDB.update_task(current_task)

            #--- Update position in current task
            self.update_positioning(current_task.get_id())

    def command_finish_task(self, secondary_command):
        #--- Secondary Tasks Empty
        if len(secondary_command) == 0:
            #--- Finish the task
            self.working_task.finish()

            #--- Update database
            self.task_interfaceDB.update_task(self.working_task)

            task_id = self.working_task.get_id()

        else:
            task_id = int(secondary_command[0])

            for current_task in self.current_tasks:
                if current_task.get_id() == task_id:
                    current_task.finish()

            #--- Update database
            self.task_interfaceDB.update_task(current_task)

            #--- Update position in current task
            self.update_positioning(current_task.get_id())

        #--- Drop the Taks from Myday
        #--- Get open tasks
        open_tasks = self.myday_interfaceDB.get_open_myday()
        for task in open_tasks:
            if task[0] == task_id:
                #--- Task finished is on myday, so we deleted
                self.myday_interfaceDB.delete_myday_task(task_id)

    def command_create(self,secondary_command):
        """
        Create a new cluster or a new tag depending of the second word

        'create cluster <clustar_name>'
        'create tag <tag_name>'
        """

        #--- Check to create a cluster
        if secondary_command[0] == 'cluster':
            cluster_name = secondary_command[1:]
            cluster_name = self.helper.convert_list_to_string(cluster_name)

            #--- Add it into the database
            self.cluster_interfaceDB.insert_cluster(cluster_name)


        #--- Check to create a tag
        elif secondary_command[0] == 'tag':
            pass

        #--- If it's nothing raise a message
        else:
            self.helper.printer(f"[ERROR] The sub-command '{secondary_command[0]}' is not valid.", 'red')
            self.helper.printer(f"Available sub-command to mix with 'create':")
            print("|--- 'create cluster my new cluster': creates a new cluster")
            print("|--- 'create tag my new tag': creates a new tag")

    def command_myday(self, secondary_command):
        """
        'myday 9 81 38 29 17'
        secondary_command= ['9', '81', '38', '29', '17']
        """
        # ----- Adding tasks to myday -----
        if secondary_command[0] == "drop":
            #-- Exclude the sub command
            secondary_command.pop(0)

            #-- Exclude each task ID in the secondary command
            for element in secondary_command:
                #-- Get the ID
                task_id = int(element)

                #-- Delete task id
                self.myday_interfaceDB.delete_myday_task(task_id)
        
        else:
            #--- Get tasks ID and convert into int
            tasks_ids = []
            for element in secondary_command:
                task_id = int(element)
                tasks_ids.append(task_id)

                #--- Get property for that task id
                properties = self.task_interfaceDB.get_property(task_id)
                task_name = properties[1]
                cluster_name = properties[5]

                #--- Inser that tasks info into myday table
                self.myday_interfaceDB.insert_myday(task_id, task_name, cluster_name)

    def command_switch(self, secondary_command):
        """
        switch task
        switch finance
        switch daily
        """
        
        #--- Take the name of swicthing tracking
        self.next_tracking = secondary_command[0]
        
        #--- Kill the condition of the main loop
        self.alive = False

        self.helper.printer(f"---- Swtiching to Tracking '{self.next_tracking}' ----", 'brown')

    def command_set(self, secondary_command):
        """
        1. Start task without a finish 
        2. Didn't start the task but it was already done
        
        > set task_id <clean_time>

        """
        try:
            #--- Extract infos from the secondary command
            id = secondary_command[0]
            clean_time = int(secondary_command[1]) #minutes

            #--- Convert the clean time in seconds
            clean_time = clean_time * 60

            #--- Get properties of the taks
            task_property = self.task_interfaceDB.get_property(id)

            #--- Create task object
            task = Task(
                name= task_property[1],
                id= id,
                tags= task_property[4],
                cluster= task_property[5]
            )

            #--- Set the clean time worked
            task.set_worked_clean(clean_time)

            #--- Reset the start and finish time
            task.set_manual_edited()

            #--- Update the task in the database
            self.task_interfaceDB.update_task(task)

            #--- Also remove it from myday if it was there
            self.myday_interfaceDB.delete_myday_task(task.get_id())
                
        except:
            self.helper.printer(f"[ERROR] Something went wrong while setting the task with ID: {secondary_command[0]} to clean time: {secondary_command[1]}", 'red')

    def command_plot(self, secondary_commnad):
        """
        Plot commands:
        - plot: plot the whole overview of all the clusters (how many minutes worked for each cluster, maybe a pizza or area graph or bar graph)
        - plot evolution: plot the number of tasks and amount of hours worked each day 
        """        
        if len(secondary_commnad) == 0:
            #--- Plot the whole overview of all the clusters
            self.plotter.plot_clusters_overview()
        elif secondary_commnad[0] == 'evolution':
            #--- Plot the evolution of the time worked
            self.plotter.plot_evolution()


    def command_kill(self, secondary_command):

        if self.working_task != None and self.working_task.get_end_string() == None:
            #--- Forced finish the current task
            self.working_task.finish()
            task_id = self.working_task.get_id()
            #--- Drop the Taks from Myday
            #--- Get open tasks
            open_tasks = self.myday_interfaceDB.get_open_myday()
            for task in open_tasks:
                if task[0] == task_id:
                    #--- Task finished is on myday, so we deleted
                    self.myday_interfaceDB.delete_myday_task(task_id)
                    
            self.helper.printer(f"[WARNING] Task '{self.working_task.get_name()}' finished by force!", time= True, color= 'brown')

        self.helper.kill(self.name)

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
    
    def update_positioning(self, id):
        for task in self.current_tasks:
            if task.get_id() == id:
                index= self.current_tasks.index(task)
                self.current_tasks.pop(index)
                self.current_tasks.append(task)

    def check_clusters(self,cluster_name):
        flag_cluster_exists = False

        if cluster_name == None:
            self.helper.printer(f"[ERROR] Not possible to create a tasks without a cluster", 'red')
            self.helper.printer(f"Consider using 'add in <cluster_name> <task_name>' for the first add")
            self.helper.printer(f"For more help use the command 'help'")

        else:
            clusters = self.cluster_interfaceDB.get_clusters()

            for cluster in clusters:
                if cluster[1] == cluster_name:
                    flag_cluster_exists = True
            
            if flag_cluster_exists == False:
                self.helper.printer(f"[ERROR] Cluster {cluster_name} not exists!", 'red')
                self.commands_store['show'](['clusters'])
                self.helper.printer(f"If the desired cluster is not within the existing ones, consider creating a new one: 'create cluster {cluster_name}'")
        
        return flag_cluster_exists