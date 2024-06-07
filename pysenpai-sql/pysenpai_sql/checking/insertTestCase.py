import sqlite3

import pysenpai.callbacks.convenience as convenience
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.messages import load_messages, Codes
from pysenpai.output import output
from pysenpai_sql.checking.tests import *

class SQLInsertTestCase(SQLTestCase):
    
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
                 show_answer_difference=True):
        
        self.ref_query_result = ref_query_result
        self.order = order
        self.selected_variables = selected_variables
        self.distinct = distinct
        self.show_answer_difference = show_answer_difference
        
        super().__init__(
            ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters
        )

    def feedback(self, res, descriptions):

        if self.selected_variables != None:
            incorrect_variables = evaluate_variables(descriptions, self.ref_query_result)
            if incorrect_variables:
                yield incorrect_variables, None

        return super().feedback(res, descriptions)  

    def wrap(self, ref_answer, student_answer, lang, msgs, test_query):
        # Run student and reference querys and return answers
        # Insert and update are both tested with this

        # Open student answer
        try :
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

            cursor.execute(sql_script)

            conn.commit()

            res = getLastInsertedRow(cursor, sql_script)

            try:
                result_list = [list(row) for row in res][0] # Arrange result to list
            except IndexError as e:
                output(msgs.get_msg("UnidentifiableRecord", lang), Codes.ERROR)
                return 0, 0, None

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
       
            cursor2.execute(ref_answer)

            conn2.commit()

            ref = getLastInsertedRow(cursor2, ref_answer) 
            self.ref_query_result = ref
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None
        
        return ref, res, result_list

def getLastInsertedRow(cursor, query):
    id_of_inserted = cursor.lastrowid

    table_name = query.split()[2]

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