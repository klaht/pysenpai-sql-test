import sqlite3
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

    Args:
    test object: The SQLTestCase object.
    (
        ref_result (str): The reference result for comparison.
        args (list, optional): Additional arguments for the test case. Defaults to None.
        inputs (list, optional): Input values for the test case. Defaults to None.
        data (dict, optional): Additional data for the test case. Defaults to None.
        weight (int, optional): The weight of the test case. Defaults to 1.
        tag (str, optional): A tag for the test case. Defaults to "".
        validator (function, optional): A function to validate the result. Defaults to convenience.parsed_result_validator.
        output_validator (function, optional): A function to validate the output. Defaults to None.
        eref_results (dict, optional): Expected reference results for comparison. Defaults to None.
        internal_config (dict, optional): Internal configuration for the test case. Defaults to None.
        presenters (list, optional): Presenters for the test case. Defaults to None.
        ref_query_result (str, optional): The reference query result. Defaults to None.
        order (str, optional): The order of the query result. Defaults to None.
        selected_variables (list, optional): The selected variables in the query. Defaults to None.
        distinct (bool, optional): Whether to use DISTINCT in the query. Defaults to True.
        show_answer_difference (bool, optional): Whether to show the difference between the reference and student answers. Defaults to True.
        exNumber (int, optional): The exercise number. Defaults to 0.)
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
                 distinct=True,
                 show_answer_difference=True,
                 exNumber=0):
        """
        Initializes a new instance of the SQLAlterTestCase class.

        Args:
            ref_result (str): The reference result for comparison.
            args (list, optional): Additional arguments for the test case. Defaults to None.
            inputs (list, optional): Input values for the test case. Defaults to None.
            data (dict, optional): Additional data for the test case. Defaults to None.
            weight (int, optional): The weight of the test case. Defaults to 1.
            tag (str, optional): A tag for the test case. Defaults to "".
            validator (function, optional): A function to validate the result. Defaults to convenience.parsed_result_validator.
            output_validator (function, optional): A function to validate the output. Defaults to None.
            eref_results (dict, optional): Expected reference results for comparison. Defaults to None.
            internal_config (dict, optional): Internal configuration for the test case. Defaults to None.
            presenters (list, optional): Presenters for the test case. Defaults to None.
            ref_query_result (str, optional): The reference query result. Defaults to None.
            order (str, optional): The order of the query result. Defaults to None.
            selected_variables (list, optional): The selected variables in the query. Defaults to None.
            distinct (bool, optional): Whether to use DISTINCT in the query. Defaults to True.
            show_answer_difference (bool, optional): Whether to show the difference between the reference and student answers. Defaults to True.
            exNumber (int, optional): The exercise number. Defaults to 0.
        """
        
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
        """
        Provides feedback for the test case.

        Args:
            res (str): The result of the student's query.
            descriptions (list): Descriptions of the feedback.

        Yields:
            tuple: A tuple containing the column data result and None.
        """
        column_data_result = compare_column_data(res, self.ref_query_result)
        if column_data_result != None:
            yield column_data_result, None

        return super().feedback(res, descriptions)  

    def wrap(self, ref_answer, student_answer, lang, msgs, test_query, insert_query):
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
        # Open student answer
        try:
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
