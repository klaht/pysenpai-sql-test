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

class SQLCreateTestCase(SQLTestCase):
    
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
                 student_answer=None,
                 insert_query=None,
                 exNumber=0):
        
        super().__init__(
            ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters
        )
        
        self.ref_query_result = ref_query_result
        self.order = order
        self.selected_variables = selected_variables
        self.distinct = distinct
        self.show_answer_difference = show_answer_difference
        self.student_answer = student_answer
        self.insert_query = insert_query
        self.exNumber = exNumber
        
    def feedback(self, res, descriptions):
        
        if self.order != None:
            incorrect_order = assertOrder(res, self.order)
            if incorrect_order:
                yield incorrect_order, None

        if self.selected_variables != None:
            incorrect_variables = assertSelectedVariables(descriptions, self.selected_variables)
            if incorrect_variables:
                yield incorrect_variables, None
            
        if self.distinct != None:
            incorrect_distinct = assertDistinct(res)
            if incorrect_distinct:
                yield incorrect_distinct, None

        if self.show_answer_difference:
            names = []
            for result in res:
                names.append(result[0])
            correctAmount, output = evaluateAmount(names, self.ref_query_result, self.exNumber)
            if correctAmount:
                yield correctAmount, output
                
        checkPrimary = checkPrimaryKey(self.student_answer, self.insert_query)
        if checkPrimary != None:
            yield checkPrimary, None

        return super().feedback(res, descriptions)
        
    def wrap(self, ref_answer, student_answer, lang, msgs, test_query, insert_query):
        # Run student and reference querys and return answers
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
            
            cursor.executescript(sql_script)
            
            # Insert to created table
            cursor.executescript(insert_query)
            # column_names = [column[0] for column in cursor.description]
        
            cursor.execute(test_query)
            
            res = cursor.fetchall()

            cursor.execute("DROP table testtable")

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
       
            cursor2.executescript(ref_answer)

            # Insert to created table
            cursor2.executescript(insert_query)

            cursor2.execute(test_query)
            ref = cursor2.fetchall()
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""
        
        return ref, res, ""