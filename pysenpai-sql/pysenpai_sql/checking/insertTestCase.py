import sqlite3
import re

import pysenpai.callbacks.convenience as convenience
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.messages import load_messages, Codes
from pysenpai.output import output
from pysenpai_sql.checking.tests import *

class SQLInsertTestCase(SQLTestCase):
    """
    A test case class for testing SQL insert queries.
    """

    def wrap(self, ref_answer, student_answer, lang, msgs):
        """
        Wraps the test case by running the student and reference queries and returning the answers.

        Args:
            ref_answer (str): The reference answer.
            student_answer (str): The student answer.
            lang (str): The language.
            msgs (Any): The messages.
            test_query (str): The test query.

        Returns:
            Tuple: The reference answer, student answer, and result list.
        """

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")

            cursor = conn.cursor()

            cursor.execute(student_answer)

            conn.commit()

            res = getLastInsertedRow(cursor, student_answer)

            try:
                result_list = [list(row) for row in res][0] # Arrange result to list
            except IndexError as e:
                output(msgs.get_msg("UnidentifiableRecord", lang), Codes.ERROR)
                return 0, 0

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
       
            cursor2.execute(ref_answer)

            conn2.commit()

            ref = getLastInsertedRow(cursor2, ref_answer) 
            self.ref_query_result = ref
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0
        
        return ref, res

def get_table_name(query):
    return re.search(r"^INSERT\s+INTO\s+`?(\w+)`?\s*", query, re.IGNORECASE).group(1)

def getLastInsertedRow(cursor, query):
    
    """
    Retrieves the last inserted row from the specified table.

    Args:
        cursor (Cursor): The database cursor object.
        query (str): The SQL query used to insert the row.

    Returns:
        tuple: The matching row from the table.

    Raises:
        IndexError: If no matching row is found or if multiple matching rows are found.
    """

    id_of_inserted = cursor.lastrowid

    table_name = get_table_name(query)

    columns_query = "PRAGMA table_info(" + table_name + ")"

    columns = cursor.execute(columns_query).fetchall()

    for column in columns:
        if column[5]:
            try:
                test_query = "SELECT * FROM " + table_name + " WHERE " + column[1] + "=" + str(id_of_inserted)
                cursor.execute(test_query)
                matchingId = cursor.fetchall()
                assert len(matchingId) == 1

                return matchingId
            except Exception:
                raise IndexError
