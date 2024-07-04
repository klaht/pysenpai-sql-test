import importlib
import io
import sqlite3
import sys
from pysenpai.messages import Codes
import re

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import output
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.testcase import SQLTestCase

class SQLCreateTestCase(SQLTestCase):

        
    def wrap(self, ref_answer, student_answer, lang, msgs):
        """
        Wraps the test case by running the student and reference queries and returning the answers.

        Args:
            ref_answer (Any): The reference answer for the test case.
            student_answer (Any): The student answer for the test case.
            lang (str): The language for the test case.
            msgs (Any): The messages for the test case.
            test_query (Any): The test query for the test case.
            insert_query (Any): The insert query for the test case.

        Returns:
            Tuple: A tuple containing the result, reference answer, and additional information.
        """
        # Run student and reference queries and return answers
        # Insert and update are both tested with this

        # Open student answer
        try :
            sql_file = open(student_answer, 'r')
            sql_script = sql_file.read()
        except FileNotFoundError as e:
            output(msgs.get_msg("FileOpenError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
            
            if sql_script.__contains__(';'):
                sql_script = sql_script.replace(';', '')
            
            cursor.executescript(sql_script)
            res = get_column_data(cursor, sql_script)

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return "ForMoreTestsIgnoreThis", "notCorrect", ""
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
       
            cursor2.executescript(ref_answer)
            ref = get_column_data(cursor2, ref_answer)

            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        #Add table name to the comparison list
        res.append(get_table_name(sql_script))
        ref.append(get_table_name(ref_answer))



        #TODO Different validator for CREATE queries
        return ref, res, ""

def get_table_name(query):
    return re.search("CREATE\s+TABLE\s+(IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*", query, flags=re.IGNORECASE).group(2)

def get_column_data(cursor, query):
    table_name = get_table_name(query)

    columns_query = "PRAGMA table_info(" + table_name + ")"

    columns = cursor.execute(columns_query).fetchall()

    return columns

def compare_column_data(ref, ans):
    try:
        for i, column in enumerate(ref):
            if column != ans[i]:
                return False
    except IndexError:
        return False
    
    return True

    
