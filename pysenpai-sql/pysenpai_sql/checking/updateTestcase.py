import sqlite3
import re

import pysenpai.callbacks.convenience as convenience
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.messages import load_messages, Codes
from pysenpai.output import output
from pysenpai_sql.checking.tests import *

class SQLUpdateTestCase(SQLTestCase):
    
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
        incorrect_variables, output = evaluate_updated_values(self.ref_query_result, self.field_names)
        if incorrect_variables:
            yield incorrect_variables, output

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
            #cursor.execute(test_query)
            #res = cursor.fetchall()

            #Get ids affected by the update
            ans_affected_ids = get_affected_row_ids(cursor, sql_script)

            #Execute updated
            cursor.execute(sql_script)

            #Get rows with previously fetched ids
            res = get_rows_with_ids(cursor, sql_script, ans_affected_ids)

            self.field_names = [i[0] for i in cursor.description]


            try:
                result_list = [list(row) for row in res][0] # Arrange result to list
            except IndexError as e:
                output(msgs.get_msg("UnidentifiableRecord", lang), Codes.ERROR)
                return 0, 0, None

            answer_row_count = cursor.rowcount

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
       


            ref_affected_ids = get_affected_row_ids(cursor2, ref_answer)

            cursor2.execute(ref_answer)

            ref = get_rows_with_ids(cursor2, ref_answer, ref_affected_ids) 

            #cursor2.execute(test_query)
            #ref = cursor2.fetchall()
            self.ref_query_result = ref

            reference_row_count = cursor.rowcount
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None
        
        if answer_row_count != reference_row_count:
            return 0, 0, None

        return ref, res, result_list

def get_affected_row_ids(cursor: sqlite3.Cursor, query):
    where_clause = re.split("where", query, maxsplit=1, flags=re.IGNORECASE)[1]
    primary_key = getTablePrimaryKey(cursor, query)

    affected_query = "SELECT " + primary_key + " FROM " + query.split()[1] + " WHERE " + where_clause

    cursor.execute(affected_query)

    return cursor.fetchall()

def getTablePrimaryKey(cursor, query):
    table_name = query.split()[1]

    columns_query = "PRAGMA table_info(" + table_name + ")"

    columns = cursor.execute(columns_query).fetchall()

    for column in columns:
        if column[5]:
            try:
                return column[1]
            except Exception as e:
                raise IndexError

def get_rows_with_ids(cursor, query, ids):
    try:  
        primary_key = getTablePrimaryKey(cursor, query)
        select_query = "SELECT * FROM " + query.split()[1] + " WHERE " + primary_key + " IN " +  ids_to_string(ids) 

        cursor.execute(select_query)

        return cursor.fetchall()
    except Exception as e:
        print(e)

def ids_to_string (ids):
    query_str = "("
    for id in ids:
        query_str += str(id[0]) + ", "

    #remove last comma
    return query_str[:-2] + ")"

