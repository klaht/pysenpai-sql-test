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

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()

            affected_table = get_table_name(ref_answer)

            res = run_query_and_get_changed_rows(cursor, student_answer, affected_table)

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()

            ref = run_query_and_get_changed_rows(cursor2, ref_answer, affected_table)

            self.ref_query_result = ref

            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0
        
        self.feedback_params['res_affected_ids'] = get_affected_row_ids(res)
        self.feedback_params['correct_affected_ids'] = get_affected_row_ids(ref)

        return ref, res

def run_query_and_get_changed_rows(cursor:sqlite3.Cursor, query:str, affected_table: str):
    changed_rows = []

    orig_content = get_table_contents(cursor, query, affected_table)
    cursor.execute(query)
    updated_content = get_table_contents(cursor, query, affected_table)

    for i, orig_row in enumerate(orig_content):
        if updated_content[i] != orig_row:
            changed_rows.append(updated_content[i])

    return changed_rows

def get_table_contents(cursor: sqlite3.Cursor, query: str, affected_table: str):
    select_query = "SELECT * FROM " + affected_table

    cursor.execute(select_query)

    return cursor.fetchall()

def get_table_name(query):
    return re.search(r"UPDATE\s+`?(\w+)`?\s+SET", query, re.IGNORECASE).group(1)
    

def get_affected_row_ids(rows: list):
    ids = []
    """
    Get affected ids from rows.
    Assume that index 0 is ID
    """

    for val in rows:
        ids.append(val[0])

    return ids
