import sqlite3
import re
import pysenpai.core as core
# from pysenpai.messages import Codes

from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.messages import load_messages, Codes
import pysenpai.callbacks.convenience as convenience
from pysenpai_sql.checking.tests import *
import pysenpai.utils.checker as utils
from pysenpai.output import output
from pysenpai.exceptions import OutputParseError

class SQLDeleteTestCase(SQLTestCase):
    def wrap(self, ref_answer, student_answer, lang, msgs):
        """
        Wraps the test case with the student's answer.

        Args:
            ref_answer (Any): The reference answer.
            student_answer (Any): The student's answer.
            lang (str): The language of the test case.
            msgs (Any): Messages for the test case.

        Returns:
            Tuple[Any, Any, str]: A tuple containing the result, reference, and an empty string.
        """

        # Run student answer
        try:
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
            cursor.execute(student_answer)

            res = get_table_contents(cursor, student_answer)
            conn.commit() 
        
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        # Run reference answer
        try:
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
            cursor2.execute(ref_answer)

            ref = get_table_contents(cursor2, ref_answer)
            
            conn2.commit()
        
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        return ref, res, ""


def get_table_contents(cursor: sqlite3.Cursor, query: str):
    table_name = query.split()[2]
    select_query = "SELECT * FROM " + table_name

    cursor.execute(select_query)

    return cursor.fetchall()

