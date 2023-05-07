import sqlite3
from .helper import Helper
from .components import Task, FinEvent, FinCategory

class interfaceDB():
    def __init__(self, name):
        self.helper = Helper()
        #--- Name of the interface
        self.name = name

        #--- Database Path Assigned
        if name == "task" or name == "cluster" or name == "myday":
            self.namedb = f"databases/TTtracking.db"
        elif name == "fin":
            self.namedb = f"databases/FinTracking.db"
        
        self.helper.create_file("databases")
        
        #--- Table creation
        if name == "task":
            self.create_task_table()

        if name == "cluster":
            self.create_cluster_table()
    
        if name == "myday":
            self.create_myday_table()
    
        if name == "fin":
            self.create_finance_table()
            self.create_category_table()
    
    
    
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
                SELECT task_id, name, cluster FROM task_table WHERE start_string IS NULL
                """
            ).fetchall()
            #tasks = self.helper.convert_tuple_vector_to_list(tasks)
            return tasks
    
    # ------ Show idle tasks (started but not finish) ------
    def get_idle_tasks(self):
        """
        Search for tasks with a started different than None but with a finish equal to None
        """
    
        with sqlite3.connect(self.namedb) as db:
            tasks = db.execute(
                """
                SELECT task_id, name, cluster FROM task_table WHERE start_string IS NOT NULL AND end_string IS NULL
                """
            ).fetchall()

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

    def delete_myday_task(self, task_id):
        # Open a connection to the database
        with sqlite3.connect(self.namedb) as db:
            cursor = db.cursor()
            query = "DELETE FROM myday_table WHERE task_id = ?"
            cursor.execute(query, (task_id,))
            db.commit()

            query2 = "SELECT * FROM myday_table WHERE task_id = ?"
            task = cursor.execute(query2, (task_id,)).fetchall()
            if len(task) > 0:
                print(f"Deleted row with task id {task_id} from myday_table.")

    # ============== FINANCE MANAGEMENT ==============
    def create_finance_table(self):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS finance_table (
                finance_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                type TEXT,
                value REAL,
                date TEXT
                )
                """
            )

    def create_category_table(self):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS category_table (
                category_id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                budget INTEGER
                )
                """
            )
    
    def insert_finance(self, finevent):
        with sqlite3.connect(self.namedb) as db:
            name = finevent.get_name()
            category = finevent.get_category()
            type = finevent.get_type()
            value = finevent.get_value()
            date = finevent.get_date()
            
            db.execute(
                """
                INSERT INTO finance_table (name, category, type, value, date)
                VALUES (?, ?, ?, ?, ?)
                """, (name, category, type, value, date)
            )

    def insert_category(self, name, type, budget):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                INSERT INTO category_table (name, type, budget)
                VALUES (?, ?, ?)
                """, (name,type,budget)
            )

    def get_category(self, name):
        with sqlite3.connect(self.namedb) as db:
            category = db.execute(
                """
                SELECT * FROM category_table WHERE name = ?
                """, (name,)
            ).fetchone()
        
        if category is None:
            return None
        else:
            category = FinCategory(name=category[1], type=category[2], budget=category[3], id=category[0])
            
            return category

    def get_categories(self):
        with sqlite3.connect(self.namedb) as db:
            categories = db.execute(
                """
                SELECT * FROM category_table
                """
            ).fetchall()

        fincategories = []
        for category in categories:
            fincategories.append(FinCategory(name=category[1], type=category[2], budget=category[3], id=category[0]))

        return fincategories

    def update_category(self, name, budget):
        with sqlite3.connect(self.namedb) as db:
            db.execute(
                """
                UPDATE category_table SET budget = ? WHERE name = ?
                """, (budget, name)
            )

    def get_week_expenses(self):
        (first_week_day, last_week_day) = self.helper.get_week()

        with sqlite3.connect(self.namedb) as db:
            expenses = db.execute(
                f"""
                SELECT * FROM finance_table WHERE type = 'exp' AND
                date BETWEEN '{first_week_day}' AND '{last_week_day}'
                """
            ).fetchall()

        if expenses is None:
            return None
        else:
            #--- Creat FinEvents
            finevents = []
            for expense in expenses:
                expense = FinEvent(name= expense[1], category= expense[2], type= expense[3], value= expense[4], date= expense[5], id= expense[0])
                finevents.append(expense)        
            
            return finevents
