
import re
import pysenpai.core as core
# from pysenpai.messages import Codes

from pysenpai_sql.checking.testcase import SQLSelectTestCase, run_sql_test_cases
from pysenpai_sql.callbacks.convenience import parsed_list_sql_validator
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError
from pysenpai_sql.core import load_sql_module
from datasetup import init_db
from pysenpai.output import output
from pysenpai_sql.checking.tests import *
from pysenpai_sql.checking.feedback_messages import create_feedback_messages

msgs = core.TranslationDict()
float_pat = re.compile("(-?[0-9]+\\.[0-9]+)")

create_feedback_messages(msgs)

class MainTestCase(SQLSelectTestCase):



    def __init__(self, ref_result, validator):

        '''''
        Basic test details (order, selected_vars, distinct values) are set here in the constructor
        For assignment specific tests, implement them in the feedback() method

        '''''
        super().__init__(
            ref_result=ref_result, validator=validator, order="ASC", selected_variables=["name"], distinct=True
        )

    def parse(self, output):
        res = utils.find_first(float_pat, output, float)
        if res is None:
            raise OutputParseError(msgs.get_msg("fail_no_output", lang))
        return res

    def feedback(self, res, descriptions):
        yield from super().feedback(res, descriptions)
        try:

            names = []
            for result in res:
                names.append(result[0])

            correctAmount, output = evaluateAmount(names, self.ref_query_result)
            if correctAmount:
                yield correctAmount, output

        except AssertionError:
            pass

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


def ref_program():
    """
    Returns reference answer of the problem.
    """
    correct_answer = ("SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name ASC;")
    return correct_answer


if __name__ == "__main__":
    core.init_test(__file__, 1)
    correct = False
    score = 0

    # Test category SELECT, UPDATE, DELETE, INSERT, CREATE
    test_type = "SELECT"

    # SELECT query to test DELETE, INSERT, UPDATE, CREATE
    test_query = ""
    
    # INSERT query to test CREATE

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
                                    gen_program_vector,
                                    lang,
                                    custom_msgs=msgs,
                                    insert_query=insert_query,
                                    test_query=test_query)

    correct = bool(score)
    core.set_result(correct, score)