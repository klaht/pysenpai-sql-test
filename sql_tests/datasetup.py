import sqlite3

sql_file = open("data.sql", 'r')
sql_script = sql_file.read()

conn = sqlite3.connect("mydatabase1.db")
cursor = conn.cursor()
       
cursor.executescript(sql_script)

conn.commit()
conn.close()

conn2 = sqlite3.connect("mydatabase2.db")
cursor2 = conn2.cursor()
       
cursor2.executescript(sql_script)

conn2.commit()
conn2.close()

