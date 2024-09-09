import sqlite3
import re
from pysenpai.messages import Codes

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import output
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.checking.tests import *

class SQLAlterTestCase(SQLTestCase):
    """
    A test case class for SQL ALTER statements.
    """

    def wrap(self, ref_answer, student_answer, lang, msgs):
        """
        Runs the student and reference queries and returns the answers.

        Args:
            ref_answer (str): The reference answer.
            student_answer (str): The student's answer file.
            lang (str): The language of the test case.
            msgs (dict): Messages for output.
            test_query (str): The test query.
            insert_query (str): The insert query.

        Returns:
            tuple: A tuple containing the reference answer, student's answer, and an empty string.
        """
        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
            cursor.execute(student_answer)
            res = get_table_information(cursor, student_answer)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0

        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
            cursor2.execute(ref_answer)
            ref = get_table_information(cursor2, ref_answer)
            self.ref_query_result = ref
            conn2.commit()
            conn2.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0

        res.append(get_table_name(student_answer))
        ref.append(get_table_name(ref_answer))

        return ref, res

def get_table_information(cursor, query):
    """
    Get information about table columns
    Uses PRAGMA query to fetch information about the table
    """
    table_name = query.split()[2]
    columns_query = "PRAGMA table_info(" + table_name + ")"
    columns = cursor.execute(columns_query).fetchall()

    return columns

def get_table_name(query):
    return re.search("ALTER\s+TABLE\s+`?(\w+)`?\s+", query, flags=re.IGNORECASE).group(1)
