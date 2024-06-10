import os
import sqlite3


def init_db(sql_file="data.sql"):
    """
    Initializes two databases by executing the SQL script from the provided file.

    The function first deletes any existing databases, then creates new ones and populates them
    with data from the SQL script.

    Args:
        sql_file (str): The path to the SQL file. Defaults to "data.sql".

    Raises:
        sqlite3.Error: If an error occurs when interacting with the SQLite database.
    """

    try:
        delete_db('mydatabase1.db', 'mydatabase2.db')

        sql_file = open(sql_file, 'r')

        sql_script = sql_file.read()

        # Database for student's answer
        conn = sqlite3.connect("mydatabase1.db")
        cursor = conn.cursor()
            
        cursor.executescript(sql_script)

        conn.commit()
        conn.close()

        # Database for reference answer
        conn2 = sqlite3.connect("mydatabase2.db")
        cursor2 = conn2.cursor()
            
        cursor2.executescript(sql_script)

        conn2.commit()
        conn2.close()
    except sqlite3.Error as e:
        print(e)

def delete_db(db_file1, db_file2):
    
    """
    Deletes two given database files.

    Args:
        dp_file1 (str): The path to the DB file.
        dp_file2 (str): The path to the DB file.

    """
    if os.path.exists(db_file1):
        os.remove(db_file1)
    if os.path.exists(db_file2):
        os.remove(db_file2)

