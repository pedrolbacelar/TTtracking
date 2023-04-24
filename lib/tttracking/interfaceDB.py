import sqlite3

class interfaceDB():
    def __init__(self, name):
        #--- Name of the interface
        self.name = name

        #--- Database Path Assigned
        self.namedb = f"/databases/{self.name}.db"

        #--- Table creation
        if name == "task":
            self.create_task_table()
    
    # --- create a tasks table ---
    def create_task_table(self):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                f"""
                CREATE TABLE IF NOT EXIST task_table (
                task_id INTEGER PRIMARY KEY,
                name TEXT,
                tags TEXT,
                duration TEXT,
                timestamp INTEGER
                )
                """
            )
    def insert_task(self, task):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                f"""
                INSERT INTO task_table (name, tags, time, timestamp) VALUES (
                {task.get_name()}
                )
                """
            )