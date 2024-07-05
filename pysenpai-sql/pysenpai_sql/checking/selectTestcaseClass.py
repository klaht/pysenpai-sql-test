import importlib
import io
import sqlite3
import sys
from pysenpai.messages import Codes

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import output
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.testcase import SQLTestCase

class SQLSelectTestCase(SQLTestCase):
    """
    Represents a test case for SQL SELECT queries.

    Args:
        sqltestcase (SQLTestCase): The SQLTestCase object.

    """
    distinct = False # Toggle whether the query should return distinct values or not
    show_answer_difference = False # Toggle whether the query should show the difference between the reference and student query answers
    order = None # Toggle whether the query should be ordered in ascending or descending order: None = no order, "ASC" = ascending, "DESC" = descending
    exNumber = 0 # Exercise number used for exercise specific feedback
    selected_variables = None # The expected selected variables in the query result

    def wrap(self, ref_answer, student_answer, lang, msgs):

        """
        Executes the student and reference queries and returns the results.

        Args:
            ref_answer (str): The reference query to be executed.
            student_answer (str): The student query to be executed.
            lang (str): The language used for error messages.
            msgs (object): An object containing error messages.

        Returns:
            tuple: A tuple containing the reference query result, student query result, and column names.
        """
    
        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
       
            cursor.execute(student_answer)
            column_names = [column[0] for column in cursor.description]

            res = cursor.fetchall()
        
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        # Run reference answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
       
            cursor.execute(ref_answer)
            ref = cursor.fetchall()
            self.ref_query_result = ref
        
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        return ref, res, column_names