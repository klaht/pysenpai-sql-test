import sqlite3
from pysenpai.messages import Codes

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import output
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.checking.tests import *

class SQLAlterTestCase(SQLTestCase):
    
    def __init__(self, ref_result, 
                 args=None,
                 inputs=None,
                 data=None,
                 weight=1,
                 tag="",
                 validator=convenience.parsed_result_validator,
                 output_validator=None,
                 eref_results=None,
                 internal_config=None,
                 presenters=None,
                 ref_query_result=None,
                 order=None,
                 selected_variables=None,
                 distinct=True,
                 show_answer_difference=True,
                 exNumber=0):
        
        self.ref_query_result = ref_query_result
        self.order = order
        self.selected_variables = selected_variables
        self.distinct = distinct
        self.show_answer_difference = show_answer_difference
        self.exNumber = exNumber
        
        super().__init__(
            ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters
        )

    def feedback(self, res, descriptions):
        column_data_result = compare_column_data(res, self.ref_query_result)
        if column_data_result != None:
            yield column_data_result, None

        return super().feedback(res, descriptions)  

    def wrap(self, ref_answer, student_answer, lang, msgs, test_query, insert_query):
        # Run student and reference querys and return answers
    
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
       
            cursor.execute(sql_script)

            res = get_table_information(cursor, sql_script)
        
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

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
            return 0, 0, ""

        return ref, res, "" 

def get_table_information(cursor, query):
    """
    Get information about table columns
    Uses PRAGMA query to fetch information about the table
    """
    table_name = query.split()[2]
    columns_query = "PRAGMA table_info(" + table_name + ")"
    columns = cursor.execute(columns_query).fetchall()

    return columns
