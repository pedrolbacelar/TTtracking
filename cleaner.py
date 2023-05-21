import sqlite3

with sqlite3.connect("database/TTtracking.db") as db:
    cursor = db.cursor()
    # Execute the SQL statement to remove the part "edited - " from start_string column
    cursor.execute("""
        UPDATE task_table
        SET start_string = REPLACE(start_string, 'edited - ', '')
    """)

    # Commit the changes to the database
    cursor.commit()