import sqlite3
import re
from pysenpai.messages import Codes

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import output
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.testcase import SQLTestCase
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.schema_tests import *

table_regex_from_query_type = {
    "SELECT": "SELECT\s+.*?\s+FROM\s+`?(\w+)`?(\s|;|$)",
    "UPDATE": "UPDATE\s+`?(\w+)`?\s+SET",
    "CREATE": "CREATE\s+TABLE\s+(IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\(",
    "ALTER": "ALTER\s+TABLE\s+`?(\w+)`?\s+",
    "INSERT": "INSERT\s+INTO\s+`?(\w+)`?\s*",
    "DELETE": "DELETE\s+FROM\s+`?(\w+)`?(\s|;|$)"
}

class SQLMultipleQueryTestCase(SQLTestCase):
    def __init__(self, 
                 ref_result, 
                 args=None, 
                 inputs=None, 
                 data=None, 
                 weight=1, 
                 tag="", 
                 validator=defaults.result_validator, 
                 output_validator=None, 
                 eref_results=None, 
                 internal_config=None, 
                 presenters=None):
        super().__init__(
            ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters
        )
        self.ans_table_content = []
        self.ref_table_content = []
        self.ans_table_data = []
        self.ref_table_data = []
    
    def feedback(self, res, descriptions):
        #Test table schema
        primary_key_check = check_primary_key(self.ans_table_data, self.ref_table_data)
        if primary_key_check:
            yield primary_key_check, None

        data_type_check = check_column_data_types(self.ans_table_data, self.ref_table_data)
        if data_type_check != None:
            yield data_type_check, None

        column_name_check = check_column_names(self.ref_table_data, self.ref_table_data)
        if column_name_check != None:
            yield column_name_check, None

        not_null_check = check_null_values_allowed(self.ref_table_data, self.ref_table_data)
        if not_null_check != None:
            yield not_null_check, None
        
        #Test table contents row by row
        for i, row in enumerate(self.ref_table_content):
            try:
                if (row != self.ans_table_content[i]):
                    yield "incorrect_inserted_data", None
                    break
            except IndexError:
                yield "incorrect_inserted_data", None
                break

        return super().feedback(res, descriptions)
    
    def wrap(self, ref_answer, student_answer, lang, msgs):
        try :
            sql_file = open(student_answer, 'r')
            sql_script = sql_file.read()
            sql_script = sql_script.replace("\n", "")
        except FileNotFoundError as e:
            output(msgs.get_msg("FileOpenError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
            ans_affected_tables = execute_multi_line_script(sql_script, cursor)
            ans_results = create_result_dict(ans_affected_tables, cursor)

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        try:
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
            ref_affected_table = execute_multi_line_script(ref_answer, cursor2)
            ref_results = create_result_dict(ref_affected_table, cursor2)

            conn2.commit()
            conn2.close()
        

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        try:
            res, ref = create_list_for_validator(ref_results, ans_results, self)
        except KeyError as e:
            output(msgs.get_msg("incorrect_table_name", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""


        return ref, res, ""

def create_list_for_validator(ref_dict: dict, ans_dict: dict, test_class: SQLMultipleQueryTestCase):
    """
    Creates a list from two dictionaries
    """
    res = []
    ref = []

    for table, values in ref_dict.items():
        ref.append(values["content"])
        ref.append(values["data"])
        test_class.ref_table_data += ref_dict[table]['data']
        test_class.ref_table_content += ref_dict[table]['content']

        res.append(ans_dict[table]["content"])
        res.append(ans_dict[table]["data"])

        test_class.ans_table_data += ans_dict[table]['data']
        test_class.ans_table_content += ans_dict[table]['content']

    return res, ref


def execute_multi_line_script(script: str, cursor: sqlite3.Cursor):
    """
    Execute every query divided by ;
    Returns table names affected by the queries
    """
    queries = script.split(";")

    for i, query in enumerate(queries):
        queries[i] = query.strip()

    affected_tables = []
    for query in queries:
        if len(query.strip()) == 0: #Don't execute empty strings
            continue
        query_type = query.split(" ")[0]
        cursor.execute(query)
        table_name = get_table_name(query, query_type)

        affected_tables.append(table_name)
    
    return affected_tables


def create_result_dict(ans_affected_tables: list, cursor: sqlite3.Cursor):
    result_dict = {}
    for table in ans_affected_tables:
        result_dict[table] = {
            "content": get_table_content(table, cursor),
            "data": get_table_data(table, cursor)
        }
        
    return result_dict

def get_table_name(query: str, query_type: str):
    """
    Get table name from given query and query type
    Query type is used to find correct regex from dictionary 
    """
    if (query_type.upper() not in table_regex_from_query_type.keys()):
        return None

    match = re.search(table_regex_from_query_type[query_type.upper()], query, flags=re.IGNORECASE)
        
    #If group 2 doesn't exist, the query has only 1 group
    try:
        return match.group(2)
    except IndexError:
        return match.group(1)

def get_table_data(table: str, cursor: sqlite3.Cursor):
    cursor.execute("PRAGMA table_info(" + table + ")")

    return cursor.fetchall()

def get_table_content(table: str, cursor: sqlite3.Cursor):
    cursor.execute("SELECT * FROM " + table)

    return cursor.fetchall()