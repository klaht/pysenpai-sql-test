import os
import sqlite3


def init_db(sql_file='data.sql'):
    delete_db('mydatabase1.db', 'mydatabase2.db')

    sql_file = open(sql_file, 'r')
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

def delete_db(db_file1, db_file2):
    if os.path.exists(db_file1):
        os.remove(db_file1)
    if os.path.exists(db_file2):
        os.remove(db_file2)

