import pysenpai.core as core
import re
from pysenpai.messages import Codes
import os

from pysenpai_sql.checking.testcase import run_sql_test_cases
from pysenpai_sql.callbacks.convenience import parsed_list_sql_validator, duplicate_validator
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError
from pysenpai_sql.core import load_sql_module
from pysenpai_sql.datasetup.datasetup import init_db
from pysenpai_sql.checking.updateTestcase import SQLUpdateTestCase
from pysenpai.output import output

from pysenpai_sql.checking.createTestcaseClass import SQLCreateTestCase 
from pysenpai_sql.checking.selectTestcaseClass import SQLSelectTestCase 
from pysenpai_sql.checking.insertTestCase import SQLInsertTestCase 
from pysenpai_sql.checking.updateTestcase import SQLUpdateTestCase 
from pysenpai_sql.checking.SQLDeleteTestCase import SQLDeleteTestCase
from pysenpai_sql.checking.SQLAlterTestCase import SQLAlterTestCase
from pysenpai_sql.checking.SQLMultipleQueryTestCase import SQLMultipleQueryTestCase

import traceback
import sys


msgs = core.TranslationDict()
float_pat = re.compile("(-?[0-9]+\\.[0-9]+)")

msgs.set_msg("EmptyAnswer", "en", dict(
    content="The test was setup incorrectly; the reference answer is empty.",
    triggers=["student_sql_query"]
))
msgs.set_msg("EmptyAnswer", "fi", dict(
    content="Testi on asetettu väärin; viitevastaus on tyhjä.",
    triggers=["student_sql_query"]
))

msgs.set_msg("EmptyStudentAnswer", "en", dict(
    content="Your answer is empty.",
    triggers=["student_sql_query"]
))
msgs.set_msg("EmptyStudentAnswer", "fi", dict(
    content="Vastauksesi on tyhjä.",
    triggers=["student_sql_query"]
))

msgs.set_msg("InvalidCommand", "en", dict(
    content="No valid SQL command detected.",
    triggers=["student_sql_query"]
))
msgs.set_msg("InvalidCommand", "fi", dict(
    content="Validia SQL komentoa ei havaittu.",
    triggers=["student_sql_query"]
))

msgs.set_msg("UnicodeError", "en", dict(
    content="The input contains invalid characters.",
    triggers=["student_sql_query"]
))

msgs.set_msg("UnicodeError", "fi", dict(
    content="Syöte sisältää virheellisiä merkkeja.",
    triggers=["student_sql_query"]
))

def gen_program_vector(ref_query, res):

    """
    Generates a vector of test cases for the main program.
    Defines the test type based on the reference query.

    Args:
        ref_query (str): The reference query.
    
    Returns:
        list: A list of test cases. Including the reference query and the validator.

    """
    test_class = None # Test class based on assignment type
   
    # Set the test class based on the assignment type
    match assignmentType.upper():
        case "SELECT":
           
            # Set the test class by using prefered settings
            test_class = SQLSelectTestCase(
            validator=parsed_list_sql_validator,
            ref_result=ref_query,
            res_result = res)
            
        case "INSERT":
           test_class = SQLInsertTestCase(ref_result=ref_query,
            validator=parsed_list_sql_validator,
            res_result = res)
        case "CREATE":
           test_class = SQLCreateTestCase(ref_result=ref_query,
            validator=parsed_list_sql_validator,
            res_result = res)
        case "UPDATE":
           test_class = SQLUpdateTestCase(ref_result=ref_query,
            validator=parsed_list_sql_validator,
            res_result = res)
        case "DELETE":
            test_class = SQLDeleteTestCase(ref_result=ref_query,
            validator=parsed_list_sql_validator,
            res_result = res)
        case "ALTER":
            test_class = SQLAlterTestCase(ref_result=ref_query,
            validator=parsed_list_sql_validator,
            res_result = res)
        case "MULTI":
            test_class = SQLMultipleQueryTestCase(ref_result=ref_query,
            validator=parsed_list_sql_validator,
            res_result = res)
        case _:
            output(msgs.get_msg("InvalidCommand", lang), Codes.INCORRECT)
            sys.exit(1)
    

    return [test_class]

if __name__ == "__main__":

     # Parse command line arguments to get the answer and reference file names
    args, language = core.parse_command()

    msgs.update(msgs)

    correct = False
    score = 0

    init_db()  # reset database

    core.init_test(__file__, 1)

    files, lang = core.parse_command()

     # Open the answer and reference files, create a query from the reference file
    try: 
        answerFile = args[0]; referenceFile = args[1]
        st_module = load_sql_module(answerFile, lang, inputs=["0"])

        if (len(args) > 2):
            config_file = args[2]
        else:
            config_file = "setting_arguments.txt"

        reference_query = open(referenceFile).read()
        reference_query = str.replace(reference_query, "\n", "")
        #Find individual queries. If length of second query is greater than 0 assignment is "MULTI"
        queries = reference_query.split(";")

        if len(queries) >= 2 and len(queries[1].strip().split()) > 0:
            assignmentType = "MULTI"
        else:
            if (len(reference_query) == 0): # If reference query is empty
                output(msgs.get_msg("EmptyStudentAnswer", language), Codes.INCORRECT)
                sys.exit(1)

            assignmentType = reference_query.split()[0]

    except UnicodeError: 
        output(msgs.get_msg("UnicodeError", language), Codes.INCORRECT)
        sys.exit(1)

    except Exception as e:
        print(e)
        traceback.print_exc() #debug
        print("USAGE: ANSWER_FILENAME REFERENCE_FILENAME")
    
    # If the answer file exists and is not empty, run the tests
    if os.path.exists(answerFile) and os.stat(answerFile).st_size > 0:
        #Open student answer
        try :
            student_answer= open(answerFile, 'r').read()
        except FileNotFoundError as e:
            output(msgs.get_msg("EmptyStudentAnswer", lang), Codes.INCORRECT)
        if st_module: # if fails to load module, don't run tests
            score += run_sql_test_cases("program",
                                        assignmentType.upper(),
                                        answerFile,
                                        lambda: gen_program_vector(reference_query, student_answer), #needs to be callable
                                        lang, custom_msgs=msgs,
                                        config_file=config_file,
                                    )
    else:
        output(msgs.get_msg("EmptyAnswer", lang), Codes.INCORRECT)
    
    isAnswerCorrect = bool(score)
    core.set_result(isAnswerCorrect, score)