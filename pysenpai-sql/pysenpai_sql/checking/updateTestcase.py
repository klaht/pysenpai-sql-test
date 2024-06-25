import sqlite3
import re

import pysenpai.callbacks.convenience as convenience
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.messages import load_messages, Codes
from pysenpai.output import output
from pysenpai_sql.checking.tests import *

class SQLUpdateTestCase(SQLTestCase):
    """
    A test case for SQL update queries.
    """

    def wrap(self, ref_answer, student_answer, lang, msgs):
        """
        Runs the student and reference queries and returns the answers.

        Args:
            ref_answer: The reference answer.
            student_answer: The student answer.
            lang: The language of the test case.
            msgs: The messages for the test case.
            test_query: The test query.

        Returns:
            Tuple: The reference answer, student answer, and result list.
        """
        # Run student and reference queries and return answers
        # Insert and update are both tested with this

        # Open student answer
        try:
            sql_file = open(student_answer, 'r')
            sql_script = sql_file.read()
        except FileNotFoundError as e:
            print("File not found")
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")

            cursor = conn.cursor()
            # cursor.execute(test_query)
            # res = cursor.fetchall()

            # Get ids affected by the update
            self.ans_affected_ids = get_affected_row_ids(cursor, sql_script)

            # Execute updated
            cursor.execute(sql_script)

            # Get rows with previously fetched ids
            # If no rows have been affected by the query set all to empty
            res = get_rows_with_ids(cursor, sql_script, self.ans_affected_ids) if self.ans_affected_ids else []
            self.field_names = [i[0] for i in cursor.description] if res else []
            result_list = [list(row) for row in res][0] if res else []

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()

            self.ref_affected_ids = get_affected_row_ids(cursor2, ref_answer)

            cursor2.execute(ref_answer)

            ref = get_rows_with_ids(cursor2, ref_answer, self.ref_affected_ids) 

            # cursor2.execute(test_query)
            # ref = cursor2.fetchall()
            self.ref_query_result = ref

            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        return ref, res, result_list

def get_affected_row_ids(cursor: sqlite3.Cursor, query):
    """
    Get all affected row primary keys from an update query
    Splits the query at the first WHERE and uses the part after in a SELECT query
    """
    where_clause = re.split("where", query, maxsplit=1, flags=re.IGNORECASE)[1]
    primary_key = getTablePrimaryKey(cursor, query)

    affected_query = "SELECT " + primary_key + " FROM " + query.split()[1] + " WHERE " + where_clause

    cursor.execute(affected_query)

    return cursor.fetchall()

def getTablePrimaryKey(cursor, query):
    """
    Get primary key from an UPDATE query
    Uses PRAGMA query to fetch information about the table
    """
    table_name = query.split()[1]
    columns_query = "PRAGMA table_info(" + table_name + ")"
    columns = cursor.execute(columns_query).fetchall()

    for column in columns:
        if column[5]: #Primary key information is stored at index 5
            try:
                return column[1] #Index 1 stores column name
            except Exception as e:
                raise IndexError

def get_rows_with_ids(cursor, query, ids):
    """
    Get all rows from table for given ids (primary key)
    """
    primary_key = getTablePrimaryKey(cursor, query)
    select_query = "SELECT * FROM " + query.split()[1] + " WHERE " + primary_key + " IN " +  ids_to_string(ids) 
    cursor.execute(select_query)

    return cursor.fetchall()

def ids_to_string (ids):
    """
    Generates a string to be used in "WHERE ... IN" query
    """
    query_str = "("
    for id in ids:
        query_str += str(id[0]) + ", "

    #remove last comma
    return query_str[:-2] + ")"

