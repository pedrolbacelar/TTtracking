import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('databases/TTtracking.db')
cursor = conn.cursor()

# Retrieve the rows from the table
cursor.execute("SELECT start_string, end_string FROM task_table")
rows = cursor.fetchall()

# Iterate through the rows and update the start_int and end_int columns
for row in rows:
    start_string = row[0]
    end_string = row[1]

    if start_string == "02 May 2023 2023 00:28:56":
        print("This would be a problem...")
        start_string = "02 May 2023 00:28:56"

    # Parse the timestamps from the start_string if it is not None
    start_timestamp = datetime.strptime(start_string, "%d %B %Y %H:%M:%S") if start_string else None

    
    # Parse the timestamps from the end_string with optional year or keep it as None if it is None
    if end_string:
        try:
            end_timestamp = datetime.strptime(end_string, "%d %B %Y %H:%M:%S")
        except ValueError:
            # If year is missing, consider it as 2023
            end_timestamp = datetime.strptime("2023 " + end_string, "%Y %d %B %H:%M:%S")
    else:
        end_timestamp = None

    # Update the start_int and end_int columns with the parsed timestamps or None
    cursor.execute("UPDATE task_table SET start_int = ?, end_int = ? WHERE start_string = ? AND end_string = ?",
                   (start_timestamp.timestamp() if start_timestamp else None, end_timestamp.timestamp() if end_timestamp else None, start_string, end_string))

# Commit the changes and close the connection
conn.commit()
conn.close()
