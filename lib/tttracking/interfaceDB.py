import sqlite3
from .helper import Helper


class interfaceDB():
    def __init__(self, name):
        self.helper = Helper()
        #--- Name of the interface
        self.name = name

        #--- Database Path Assigned
        self.namedb = f"databases/TTtracking.db"
        self.helper.create_file("databases")
        

        #--- Table creation
        if name == "task":
            self.create_task_table()

        if name == "cluster":
            self.create_cluster_table()
    
        if name == "myday":
            self.create_myday_table()
    # ============== TASK MANAGEMENT ==============
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
                end_string TEXT,
                targeted_time INTEGER
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
            
            if current_id == None:
                return 1
            else:
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
    
    def get_tasks_from_cluster(self,cluster_name):
        with sqlite3.connect(self.namedb) as db:
            tasks = db.execute(
                """
                SELECT task_id, name FROM task_table WHERE cluster = ? AND start_string IS NULL
                """,(cluster_name, )
            ).fetchall()

            return tasks


    # ================================================

    # ============== CLUSTER - TAG MANAGEMENT ==============
    # --- create cluster table ---
    def create_cluster_table(self):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS cluster_table (
                cluster_id INTEGER PRIMARY KEY,
                name TEXT,
                accumulated_worked_clean INTEGER,
                accumulated_stop INTEGER
                )
                """
            )
 
    # --- insert a new cluster ---
    def insert_cluster(self, cluster_name):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                INSERT INTO cluster_table (name) VALUES (?)
                """, (cluster_name,)
            )

    def get_clusters(self):
        with sqlite3.connect(self.namedb) as db:
            clusters= db.execute(
                """
                SELECT cluster_id, name FROM cluster_table
                """
            ).fetchall()

            return clusters
    
    # ============== MYDAY MANAGEMENT ==============
    def create_myday_table(self):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS myday_table (
                myday_id INTEGER PRIMARY KEY,
                task_id INTEGER,
                task_name TEXT,
                cluster_name TEXT
                )
                """
            )
    
    def insert_myday(self, task_id, task_name, cluster_name):
        with sqlite3.connect(self.namedb) as db:
            # task_id = task.get_id()
            # task_name = task.get_name()
            # cluster_name = task.get_cluster()

            db.execute(
                """
                INSERT INTO myday_table (task_id, task_name, cluster_name)
                VALUES (?, ?, ?)
                """, (task_id, task_name, cluster_name)
            )
    def get_open_myday(self):
        with sqlite3.connect(self.namedb) as db:
            tasks = db.execute(
                """
                SELECT task_id, task_name, cluster_name FROM myday_table
                """
            ).fetchall()

            return tasks


