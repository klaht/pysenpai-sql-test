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
    """
    A class representing a SQL test case for creating tables.

    Args:
        sqltestcase (SQLTestCase): The SQLTestCase object.
        (
        ref_result (Any): The reference result for the test case.
        args (Optional[Any]): Additional arguments for the test case. Default is None.
        inputs (Optional[Any]): Inputs for the test case. Default is None.
        data (Optional[Any]): Data for the test case. Default is None.
        weight (int): The weight of the test case. Default is 1.
        tag (str): The tag for the test case. Default is an empty string.
        validator (Callable): The validator function for the test case. Default is convenience.parsed_result_validator.
        output_validator (Optional[Callable]): The output validator function for the test case. Default is None.
        eref_results (Optional[Any]): The expected reference results for the test case. Default is None.
        internal_config (Optional[Any]): Internal configuration for the test case. Default is None.
        presenters (Optional[Any]): Presenters for the test case. Default is None.
        ref_query_result (Optional[Any]): The reference query result for the test case. Default is None.
        order (Optional[Any]): The order for the test case. Default is None.
        selected_variables (Optional[Any]): The selected variables for the test case. Default is None.
        distinct (Optional[Any]): The distinct value for the test case. Default is None.
        show_answer_difference (Optional[Any]): The show answer difference value for the test case. Default is None.
        student_answer (Optional[Any]): The student answer for the test case. Default is None.
        insert_query (Optional[Any]): The insert query for the test case. Default is None.
        correct_table_names (Optional[Any]): The correct table names for the test case. Default is None.
        req_column_names (Optional[Any]): The required column names for the test case. Default is None.
        exNumber (int): The exercise number for the test case. Default is 0.)

    Attributes:
        ref_query_result (Optional[Any]): The reference query result for the test case.
        order (Optional[Any]): The order for the test case.
        selected_variables (Optional[Any]): The selected variables for the test case.
        distinct (Optional[Any]): The distinct value for the test case.
        show_answer_difference (Optional[Any]): The show answer difference value for the test case.
        student_answer (Optional[Any]): The student answer for the test case.
        insert_query (Optional[Any]): The insert query for the test case.
        exNumber (int): The exercise number for the test case.
        correct_table_names (Optional[Any]): The correct table names for the test case.
        req_column_names (Optional[Any]): The required column names for the test case.
    """

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
                 distinct=None,
                 show_answer_difference=None,
                 student_answer=None,
                 insert_query=None,
                 correct_table_names=None,
                 req_column_names=None,
                 exNumber=0):
        """
        Initializes a new instance of the SQLCreateTestCase class.
        """
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
        self.correct_table_names = correct_table_names
        self.req_column_names = req_column_names
        
    def feedback(self, res, descriptions):
        """
        Provides feedback for the test case.

        Args:
            res (Any): The result of the test case.
            descriptions (Any): The descriptions for the test case.

        Yields:
            Tuple: A tuple containing the feedback message and additional information.
        """
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

        if self.correct_table_names != None:    
            tableNameCheck = checkTableName(correct_table_names=self.correct_table_names)
            if tableNameCheck != None:
                yield tableNameCheck, None

        if self.req_column_names != None and tableNameCheck == None:
            checkTableColumnNames = checkTableColumns(req_column_names=self.req_column_names)
            if checkTableColumnNames != None:
                yield checkTableColumnNames, None

        return super().feedback(res, descriptions)
        
    def wrap(self, ref_answer, student_answer, lang, msgs, test_query, insert_query):
        """
        Wraps the test case by running the student and reference queries and returning the answers.

        Args:
            ref_answer (Any): The reference answer for the test case.
            student_answer (Any): The student answer for the test case.
            lang (str): The language for the test case.
            msgs (Any): The messages for the test case.
            test_query (Any): The test query for the test case.
            insert_query (Any): The insert query for the test case.

        Returns:
            Tuple: A tuple containing the result, reference answer, and additional information.
        """
        # Run student and reference queries and return answers
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
            
            if sql_script.__contains__(';'):
                sql_script = sql_script.replace(';', '')
            
            cursor.executescript(sql_script)
            
            # Insert to created table
            #cursor.executescript(insert_query)
            # column_names = [column[0] for column in cursor.description]
        
            #cursor.execute(test_query)
            
            res = cursor.fetchall()
            answer_columns = get_column_data(cursor, sql_script)

            #cursor.execute("DROP table testtable")

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return "ForMoreTestsIgnoreThis", "notCorrect", ""
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
       
            cursor2.executescript(ref_answer)

            ref_columns = get_column_data(cursor2, ref_answer)

            # Insert to created table
            #cursor2.executescript(insert_query)

            #cursor2.execute(test_query)
            ref = cursor2.fetchall()
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        try :
            sql_file = open(student_answer, 'r')
            sql_script = sql_file.read()
        except FileNotFoundError as e:
            return "file_open_error"
            
        # Run student answer
        """
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
            primary_key_test = "INSERT INTO testtable VALUES (1, 'testi2')"

            cursor.executescript(sql_script)
            conn.commit()
            # Insert to created table
            cursor.executescript(insert_query)

            cursor.execute(primary_key_test)            

            conn.commit()
            cursor.close()
            conn.close()
            
        except sqlite3.IntegrityError as e:
            return ref, res, ""
        """

        if compare_column_data(ref_columns, answer_columns):
            return res, ref, ""
        
        #TODO Add tests for primary key
        #output(msgs.get_msg("missing_primarykey", lang), Codes.INCORRECT)
        return 0, 0, ""

def get_column_data(cursor, query):
    table_name = query.split()[2]

    columns_query = "PRAGMA table_info(" + table_name + ")"

    columns = cursor.execute(columns_query).fetchall()

    return columns

def compare_column_data(ref, ans):
    try:
        for i, column in enumerate(ref):
            if column != ans[i]:
                return False
    except IndexError:
        return False
    
    return True

    
