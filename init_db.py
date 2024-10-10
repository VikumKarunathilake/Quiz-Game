import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('quiz_app.db')
cursor = conn.cursor()

# Read the SQL file and execute its content
with open('schema.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)
conn.commit()
conn.close()
