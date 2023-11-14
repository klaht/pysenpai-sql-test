
import re
import pysenpai.core as core
# from pysenpai.messages import Codes

from pysenpai_sql.checking.testcase import SQLQueryTestCase, run_sql_test_cases
from pysenpai_sql.callbacks.convenience import parsed_list_sql_validator
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError
from pysenpai_sql.core import load_sql_module

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


class MainTestCase(SQLQueryTestCase):

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
    correct_answer = ("UPDATE exhibition SET numberOfVisitors = 14000, "
                      "numberOfOnlineVisitors = 50000 "
                      "WHERE title = 'Navigating North' AND "
                      "startDate = '2022-10-07' AND "
                      "endDate = '2023-04-02' AND "
                      "locationId = (SELECT locationId FROM location "
                      "WHERE name = 'Museum of Contemporary Art Kiasma') "
                      "AND isOnlineExhibition = 1; ")
    return correct_answer


if __name__ == "__main__":
    correct = False
    score = 0

    # Test category SELECT, UPDATE, DELETE, INSERT, CREATE
    test_type = "UPDATE"

    # SELECT query to test DELETE, INSERT, UPDATE, CREATE
    test_query = ("SELECT title, numberOfVisitors, numberOfOnlineVisitors "
                  "FROM Exhibition;")

    # INSERT query to test CREATE
    insert_query = ""

    core.init_test(__file__, 1)

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
                                    lang, custom_msgs=msgs,
                                    insert_query=insert_query,
                                    test_query=test_query)

    correct = bool(score)
    core.set_result(correct, score)
