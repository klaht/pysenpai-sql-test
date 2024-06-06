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
                 field_names = None,
                 order=None,
                 selected_variables=None,
                 distinct=True,
                 show_answer_difference=True):
        
        self.ref_query_result = ref_query_result
        self.field_names = field_names
        self.order = order
        self.selected_variables = selected_variables
        self.distinct = distinct
        self.show_answer_difference = show_answer_difference
        
        super().__init__(
            ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters
        )

    def feedback(self, res, descriptions):
        yield from super().feedback(res, descriptions)
        try:
            names = []
            for result in res:
                names.append(result[0])
            if names != sorted(names):
                yield ("incorrect_return_order", {})

            correct = ["name", "yearborn", "birthplace"]
            # convert to lowercase
            descriptions = [item.lower() for item in descriptions]

            incorrect_variables = descriptions != correct
            incorrect_order = (sorted(descriptions) == sorted(correct)
                               and incorrect_variables)

            if incorrect_order:
                yield ("incorrect_column_order", {})
            elif incorrect_variables:
                yield ("incorrect_selected_columns", {})

        except AssertionError:
            pass
    
    def wrap(self, ref_answer, student_answer, lang, msgs, test_query):
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
        
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        # Run reference answer
        try:
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()

            cursor2.execute(ref_answer)

            conn2.commit()
        
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        return [], [], None

