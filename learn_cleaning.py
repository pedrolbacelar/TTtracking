import sqlite3
from datetime import datetime

# Connect to the SQLite3 database
conn = sqlite3.connect('databases/LearnTracking.db')
cursor = conn.cursor()

# Retrieve the data from the "next_review" column
cursor.execute("SELECT rowid, next_review FROM cards_table")
rows = cursor.fetchall()

# Iterate through each row and convert the date format to a timestamp
for row in rows:
    rowid = row[0]
    next_review = row[1]
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(next_review, "%d %B %Y")
    # Convert the datetime object to a timestamp integer
    timestamp = int(date_obj.timestamp())
    # Update the existing "next_review_int" column with the timestamp value
    cursor.execute("UPDATE cards_table SET next_review_int = ? WHERE rowid = ?", (timestamp, rowid))

# Commit the changes and close the connection
conn.commit()
conn.close()
