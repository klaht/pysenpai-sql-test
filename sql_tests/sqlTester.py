import pysenpai.core as core
import re
from pysenpai.messages import Codes

from pysenpai_sql.checking.testcase import run_sql_test_cases
from pysenpai_sql.callbacks.convenience import parsed_list_sql_validator, duplicate_validator
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError
from pysenpai_sql.core import load_sql_module
from datasetup import init_db
from pysenpai_sql.checking.updateTestcase import SQLUpdateTestCase
from pysenpai.output import output

from pysenpai_sql.checking.createTestcaseClass import SQLCreateTestCase 
from pysenpai_sql.checking.selectTestcaseClass import SQLSelectTestCase 
from pysenpai_sql.checking.insertTestCase import SQLInsertTestCase 
from pysenpai_sql.checking.updateTestcase import SQLUpdateTestCase 
from pysenpai_sql.checking.SQLDeleteTestCase import SQLDeleteTestCase
from pysenpai_sql.checking.SQLAlterTestCase import SQLAlterTestCase

import traceback

# TODO 
#   Set messages like is done in seperate main files
#   Clean previous main files
#   Add support for database seeding files 
#   Insert queries and test queries? 

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

msgs.set_msg("too_many_return_values", "fi", dict(
    content="Tulos sisälsi liikaa palautusarvoja {output}",
    triggers=["student_sql_query"]
))

msgs.set_msg("too_many_return_values", "en", dict(
    content="The result contained too many values {output}",
    triggers=["student_sql_query"]
))

msgs.set_msg("too_little_return_values", "fi", dict(
    content="Tulos sisälsi liian vähän palautusarvoja {output}",
    triggers=["student_sql_query"]
))

msgs.set_msg("too_little_return_values", "en", dict(
    content="The result contained too low amount of values {output}", 
    triggers=["student_sql_query"]
))

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

def gen_program_vector(ref_query):

    """
    Generates a vector of test cases for the main program.
    """
    test_class = None

    # hash map?
    match assignmentType.upper():
        case "SELECT":
           test_class = SQLSelectTestCase 
        case "INSERT":
           test_class = SQLInsertTestCase 
        case "CREATE":
           test_class = SQLCreateTestCase 
        case "UPDATE":
           test_class = SQLUpdateTestCase 
        case "DELETE":
            test_class = SQLDeleteTestCase
        case "ALTER":
            test_class = SQLAlterTestCase
    v = []
    for i in range(1):
        v.append(test_class(
            ref_result=ref_query,
            validator=parsed_list_sql_validator
        ))

    return v

if __name__ == "__main__":

    args, language = core.parse_command()
    try: 
        answerFile = args[0]; referenceFile = args[1]

        reference_query = open(referenceFile).readline()
        assignmentType = reference_query.split()[0]

    except Exception as e:
        print(e)
        traceback.print_exc() #debug
        print("USAGE: ANSWER_FILENAME REFERENCE_FILENAME")


    correct = False
    score = 0

    test_query = ""

    # INSERT query to test CREATE
    insert_query = ""

    init_db()  # reset database

    core.init_test(__file__, 1)

    msgs.update(msgs)

    files, lang = core.parse_command()

    st_mname = files[0]

    st_module = load_sql_module(st_mname, lang, inputs=["0"])

    # if fails, don't run tests
    if st_module:
        score += run_sql_test_cases("program",
                                    assignmentType.upper(),
                                    st_mname,
                                    lambda: gen_program_vector(reference_query), #needs to be callable
                                    lang, custom_msgs=msgs,
                                    insert_query=insert_query,
                                    test_query=test_query)

    correct = bool(score)
    core.set_result(correct, score)
