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

class SQLSelectTestCase(SQLTestCase):
    """
    Represents a test case for SQL SELECT queries.

    Args:
        sqltestcase (SQLTestCase): The SQLTestCase object.

    """
    distinct = False # Toggle whether the query should return distinct values or not
    show_answer_difference = False # Toggle whether the query should show the difference between the reference and student query answers
    order = None # Toggle whether the query should be ordered in ascending or descending order: None = no order, "ASC" = ascending, "DESC" = descending
    exNumber = 0 # Exercise number used for exercise specific feedback
    selected_variables = None # The expected selected variables in the query result
        

    def __init__(self, ref_result, args=None, inputs=None, data=None, weight=1, tag="", validator=convenience.parsed_result_validator,
                 output_validator=None, eref_results=None, internal_config=None, presenters=None, ref_query=None):
        """
        Initializes a new instance of the SQLSelectTestCase class.
        Parameters define the extra feedback tests to be run.

        Args:
            ref_result (Any): The reference result.
            args (Optional[Any]): Additional arguments for the test case. Default is None.
            inputs (Optional[Any]): Additional inputs for the test case. Default is None.
            data (Optional[Any]): Additional data for the test case. Default is None.
            weight (int): The weight of the test case. Default is 1.
            tag (str): The tag for the test case. Default is an empty string.
            validator (Callable): The validator function for the test case. Default is convenience.parsed_result_validator.
            output_validator (Optional[Callable]): The output validator function for the test case. Default is None.
            eref_results (Optional[Any]): The expected reference results for the test case. Default is None.
            internal_config (Optional[Any]): The internal configuration for the test case. Default is None.
            presenters (Optional[Any]): The presenters for the test case. Default is None.
            ref_query_result (Optional[Any]): The expected reference query result. Default is None.
            order (Optional[Any]): The expected order of the query result. Default is None.
            selected_variables (Optional[Any]): The expected selected variables in the query result. Default is None.
            distinct (bool): Whether the query result should be distinct. Default is True.
            show_answer_difference (bool): Whether to show the difference between the answer and the reference result. Default is True.
            exNumber (int): The exercise number. Default is 0.
        """
        
        # Check if the setting_arguments.txt file exists and read the settings from it
        settings = []
        for setting in open("setting_arguments.txt", "r").readlines():
            settings.append(setting)
        
        # Check if show_answer_difference is in the settings and set the variable accordingly
        if "show_answer_difference" in settings:
            self.show_answer_difference = True
        
        # Check if exNumber is in the settings and set the variable accordingly
        for setting in settings:
            if "exNumber" in setting:
                self.exNumber = setting.split("=")[1].strip()
                break  # exit the loop once the setting is found
            
        
         # Check if reference query contains DISTINCT keyword
        if ref_query.find("DISTINCT") != -1:
            self.distinct = True
            
            # Check if reference query contains ORDER BY keyword and set the order accordingly    
        if ref_query.find("ORDER BY") != -1:
            if ref_query.find("ASC") != -1:
                self.order = "ASC"
                    
            if ref_query.find("DESC") != -1:
                self.order = "DESC"

        super().__init__(ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters)

    def feedback(self, res, descriptions, ref):
        """
        Provides feedback for the test case.
        Different feedback tests can be toggled on or off, or they can have different values.
        Some test are very test specific and some are more general.

        Args:
            (self: containing the information on which tests to run)
            res (Any): The query result.
            descriptions (Any): The descriptions.

        Yields:
            Tuple: A tuple containing the feedback message and additional information.
        """

        # Check for incorrect order
        if self.order is not None:
            incorrect_order = assertOrder(res, self.order)
            if incorrect_order:
                yield incorrect_order, None
        
        # Check for incorrect variables
        if self.selected_variables is not None:
            incorrect_variables = assertSelectedVariables(descriptions, self.selected_variables)
            if incorrect_variables:
                yield incorrect_variables, None

        # Check whether the query result is distinct
        if self.distinct is not None:
            incorrect_distinct = assertDistinct(res)
            if incorrect_distinct:
                yield incorrect_distinct, None

        # Show the difference between the answer and the reference result
        if self.show_answer_difference:
            names = []
            for result in res:
                names.append(result[0])
            correctAmount, output = evaluateAmount(names, self.ref_query_result, self.exNumber)
            if correctAmount:
                yield correctAmount, output

        return super().feedback(res, descriptions)  

    def wrap(self, ref_answer, student_answer, lang, msgs):

        """
        Executes the student and reference queries and returns the results.

        Args:
            ref_answer (str): The reference query to be executed.
            student_answer (str): The student query to be executed.
            lang (str): The language used for error messages.
            msgs (object): An object containing error messages.

        Returns:
            tuple: A tuple containing the reference query result, student query result, and column names.
        """
    
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
            column_names = [column[0] for column in cursor.description]

            res = cursor.fetchall()
        
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        # Run reference answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
       
            cursor.execute(ref_answer)
            ref = cursor.fetchall()
            self.ref_query_result = ref
        
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""

        return ref, res, column_names