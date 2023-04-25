import sqlite3
from .helper import Helper


class interfaceDB():
    def __init__(self, name):
        self.helper = Helper()
        #--- Name of the interface
        self.name = name

        #--- Database Path Assigned
        self.namedb = f"databases/{self.name}.db"
        self.helper.create_file("databases")
        

        #--- Table creation
        if name == "task":
            self.create_task_table()
    
    # --- create a tasks table ---
    def create_task_table(self):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS task_table (
                task_id INTEGER PRIMARY KEY,
                name TEXT,
                worked_clean INTEGER,
                total_stop INTEGER,
                tags TEXT,
                cluster TEXT,
                start_string TEXT,
                end_string TEXT
                )
                """
            )
    def insert_task(self, task):
        name = task.get_name()
        worked_clean = task.get_worked_time_clean()
        total_stop = task.get_stopped_time()
        tags= task.get_tags()
        cluster= task.get_cluster()
        start_string= task.get_start_timestamp()
        end_string = task.get_end_string()

        with sqlite3.connect(self.namedb) as db:
            db.execute(
                f"""
                INSERT INTO task_table (name, worked_clean, total_stop, tags,
                cluster, start_string, end_string) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,(
                name,
                worked_clean,
                total_stop,
                tags,
                cluster,
                start_string,
                end_string
                )
            )
    # ------ Show tasks without an start time ------
    def get_open_tasks(self):
        with sqlite3.connect(self.namedb) as db:
            tasks= db.execute(
                f"""
                SELECT task_id, name FROM task_table WHERE start_string IS NULL
                """
            ).fetchall()
            #tasks = self.helper.convert_tuple_vector_to_list(tasks)
            return tasks
    
    # ------ Get task property ------
    def get_property(self, id):
        with sqlite3.connect(self.namedb) as db:
            properties= db.execute(
                """
                SELECT * FROM task_table WHERE task_id=?
                """,(id,)
            ).fetchone()

            return properties

    def get_next_taks_id(self):
        with sqlite3.connect(self.namedb) as db:
            current_id= db.execute(
                """
                SELECT MAX(task_id) FROM task_table
                """
            ).fetchone()[0]

            next_id = current_id + 1
            return next_id
        
    def update_task(self, task):
        name = task.get_name()
        id = task.get_id()
        worked_clean = task.get_worked_time_clean()
        total_stop = task.get_stopped_time()
        tags= task.get_tags()
        cluster= task.get_cluster()
        start_string= task.get_start_string()
        end_string = task.get_end_string()

        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                UPDATE task_table SET name=?, worked_clean=?, total_stop=?, tags=?,
                cluster=?, start_string=?, end_string= ? WHERE task_id= ?""",(
                name,
                worked_clean,
                total_stop,
                tags,
                cluster,
                start_string,
                end_string,
                id
                )
            )

