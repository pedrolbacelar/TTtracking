from .interfaceDB import interfaceDB
from .components import Task
from .components import Tag
from .components import Cluster

class TTtracker():
    def __init__(self,name):
        self.name = name
        self.condition = True

        # ----- Database Management -----
        self.task_interfaceDB = interfaceDB("task")


        # ----- COMMANDS DICTIONARY -----



    def run(self):
        # ------ Infinity Loop ------
        while self.condition:
            command = input(f"{self.name}>> ")


    # ===================== COMMANDS FUNCTIONS =====================
    def commmand_create_task(self, name):
        new_task = Task(name= name)

