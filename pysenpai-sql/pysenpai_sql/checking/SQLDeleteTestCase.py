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
    """
    A test case class for testing SQL DELETE statements.

    Args:
    test object: The SQLTestCase object.
    (
        ref_result (Any): The reference result for comparison.
        args (Optional[Any]): Additional arguments for the test case.
        inputs (Optional[Any]): Inputs for the test case.
        data (Optional[Any]): Data for the test case.
        weight (int): The weight of the test case.
        tag (str): A tag for the test case.
        validator (Callable): A function for validating the result.
        output_validator (Optional[Callable]): A function for validating the output.
        eref_results (Optional[Any]): Expected reference results.
        internal_config (Optional[Any]): Internal configuration for the test case.
        presenters (Optional[Any]): Presenters for the test case.
        ref_query_result (Optional[Any]): Reference query result.
        field_names (Optional[Any]): Field names for the test case.
        order (Optional[Any]): Order for the test case.
        selected_variables (Optional[Any]): Selected variables for the test case.
        distinct (bool): Whether to use DISTINCT in the query.
        show_answer_difference (bool): Whether to show the difference between the answer and the reference.)

    Attributes:
        ref_query_result (Any): The reference query result.
        field_names (Any): The field names for the test case.
        order (Any): The order for the test case.
        selected_variables (Any): The selected variables for the test case.
        distinct (bool): Whether to use DISTINCT in the query.
        show_answer_difference (bool): Whether to show the difference between the answer and the reference.
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
                 field_names=None,
                 order=None,
                 selected_variables=None,
                 distinct=True,
                 show_answer_difference=True):
        """
        Initializes a new instance of the SQLDeleteTestCase class.
        """
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
        """
        Provides feedback for the test case.

        Args:
            res (Any): The result of the test case.
            descriptions (Any): Descriptions for the test case.

        Yields:
            Tuple[str, dict]: A tuple containing the feedback message and additional information.
        """
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
        """
        Wraps the test case with the student's answer.

        Args:
            ref_answer (Any): The reference answer.
            student_answer (Any): The student's answer.
            lang (str): The language of the test case.
            msgs (Any): Messages for the test case.
            test_query (Any): The test query.

        Returns:
            Tuple[Any, Any, str]: A tuple containing the result, reference, and an empty string.
        """
        try:
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

            res = get_table_contents(cursor, sql_script)

            conn.commit() 
        
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        # Run reference answer
        try:
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
            cursor2.execute(ref_answer)

            ref = get_table_contents(cursor2, ref_answer)

            conn2.commit()
        
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None

        return res, ref, ""


def get_table_contents(cursor: sqlite3.Cursor, query: str):
    table_name = query.split()[2]
    select_query = "SELECT * FROM " + table_name

    cursor.execute(select_query)

    return cursor.fetchall()

