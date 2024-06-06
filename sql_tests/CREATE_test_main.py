
from pyexpat.errors import codes
import re
import sqlite3
import pysenpai.core as core
from pysenpai.messages import Codes

from pysenpai_sql.checking.testcase import run_sql_test_cases
from pysenpai_sql.checking.createTestcaseClass import SQLCreateTestCase
from pysenpai_sql.callbacks.convenience import *
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError
from pysenpai_sql.core import load_sql_module
from datasetup import init_db
from pysenpai.output import output


msgs = core.TranslationDict()
float_pat = re.compile("(-?[0-9]+\\.[0-9]+)")

msgs.set_msg("fail_output_result", "fi", dict(
    content="Pääohjelman tulostama tulos oli väärä.",
    triggers=["student_sql_query"]
))
msgs.set_msg("fail_output_result", "en", dict(
    content="The result printed by the main program was wrong.",
    triggers=["student_sql_query"]
))

msgs.set_msg("incorrect_return_order", "fi", dict(
    content="Palautettava listaa ei järjestetty oikein.",
    triggers=["student_sql_query"]
))

msgs.set_msg("incorrect_return_order", "en", dict(
    content="The list was not arranged correctly.",
    triggers=["student_sql_query"]
))

msgs.set_msg("incorrect_selected_columns", "fi", dict(
    content="Haussa käyttettiin vääriä sarakkeita.",
    triggers=["student_sql_query"]
))

msgs.set_msg("incorrect_selected_columns", "en", dict(
    content="The query used wrong columns.",
    triggers=["student_sql_query"]
))

msgs.set_msg("incorrect_column_order", "fi", dict(
    content="Virheellinen sarakkeiden järjestys",
    triggers=["student_sql_query"]
))

msgs.set_msg("incorrect_column_order", "en", dict(
    content="Invalid column order.",
    triggers=["student_sql_query"]
))

msgs.set_msg("value_non_unique", "fi", dict(
    content="Taulukon arvo ei ole uniikki.",
    triggers=["student_sql_query"]
))

msgs.set_msg("value_non_unique", "en", dict(
    content="The value is not unique.",
    triggers=["student_sql_query"]
))


class MainTestCase(SQLCreateTestCase):

    def __init__(self, ref_result, validator):

        '''''
        Basic test details (order, selected_vars, distinct values) are set here in the constructor
        For assignment specific tests, implement them in the feedback() method

        '''''
        super().__init__(
            ref_result=ref_result,
            validator=validator,
            order=None,
            selected_variables=None,
            distinct=None,
            insert_query=primary_key_ref,
            exNumber=2,
            correct_table_names=[("testtable",)], # USE THIS FORMAT [("table1",), ("table2",)] REMEMBER THE COMMA
            req_column_names=["Id", "name"]
        )

    def parse(self, output):
        res = utils.find_first(float_pat, output, float)
        if res is None:
            raise OutputParseError(msgs.get_msg("fail_no_output", lang))
        return res

    def feedback(self, res, descriptions):
        yield from super().feedback(res, descriptions)

        
def gen_program_vector():

    """
    Generates a vector of test cases for the main program.
    """
    v = []
    for i in range(1):
        v.append(MainTestCase(
            ref_result=ref_program(),
            validator=parsed_list_sql_validator
        ))
    return v

def primary_key_ref():
    insert_query = "INSERT INTO testtable VALUES (1, 'testi2')"
    return insert_query

def ref_program():

    """
    Returns reference answer of the problem.
    """

    # Put the correct example answer here
    correct_answer = (
        "CREATE TABLE testtable "
        "(Id INTEGER PRIMARY KEY, name VARCHAR (50) NOT NULL);"
    )
    return correct_answer


def execute_test(ref_result):
    core.init_test(__file__, 1)
    correct = False
    score = 0

    # Test category SELECT, UPDATE, DELETE, INSERT, CREATE
    test_type = "CREATE"

    # SELECT query to test DELETE, INSERT, UPDATE, CREATE
    #test_query = "SELECT * FROM testtable WHERE name = 'testi'"
    test_query = ""
    
    # INSERT query to test CREATE

    #insert_query = "INSERT INTO testtable VALUES (1, 'testi')"
    insert_query = ""

    init_db() # reset database

    msgs.update(msgs)

    files, lang = core.parse_command()

    st_mname = files[0]

    st_module = load_sql_module(st_mname, lang, inputs=["0"])

    # if fails, don't run tests
    if st_module:
        score += run_sql_test_cases("program",
                                    test_type,
                                    st_mname,
                                    lambda: [MainTestCase(ref_result=ref_result, validator=parsed_list_sql_validator)],
                                    lang,
                                    custom_msgs=msgs,
                                    insert_query=insert_query,
                                    test_query=test_query)

    correct = bool(score)
    core.set_result(correct, score)


