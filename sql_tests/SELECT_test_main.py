
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

def assertAscOrder(res):
    '''Checks if the list is sorted in ascending order'''

    if res != sorted(res):
        return ("incorrect_return_order", {})
    return None

def assertSelectedVariables(res, correct):
    '''Checks if the list contains the correct variables and that they are in the correct order'''
    
    res = [item.lower() for item in res]
    
    incorrect_variables = res != correct
    incorrect_order = sorted(res) == (sorted(correct)
                                                and incorrect_variables)

    if incorrect_order:
        return ("incorrect_column_order", {})
    elif incorrect_variables:
        return ("incorrect_selected_columns", {})
    return None

class MainTestCase(SQLSelectTestCase):
    
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
            
            incorrect_order = assertAscOrder(names)
            if incorrect_order:
                yield incorrect_order
                
            correct = ["name"]
            # convert to lowercase
            print(assertSelectedVariables(names, correct))
            incorrect_variables = assertSelectedVariables(names, correct)
            if incorrect_variables:
                yield incorrect_variables

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
