
import re
import sqlite3
import pysenpai.core as core
from pysenpai.messages import Codes

from pysenpai_sql.checking.testcase import run_sql_test_cases
from pysenpai_sql.callbacks.convenience import parsed_list_sql_validator, duplicate_validator
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError
from pysenpai_sql.core import load_sql_module
from datasetup import init_db
from pysenpai_sql.checking.updateTestcase import SQLUpdateTestCase
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


class MainTestCase(SQLUpdateTestCase):

    def __init__(self, ref_result, validator):

        '''''
        Basic test details (order, selected_vars, distinct values) are set here in the constructor
        For assignment specific tests, implement them in the feedback() method

        '''''
        super().__init__(
            ref_result=ref_result, validator=validator
        )


    def parse(self, output):
        res = utils.find_first(float_pat, output, float)
        if res is None:
            raise OutputParseError(msgs.get_msg("fail_no_output", lang))
        return res

    def feedback(self, res, descriptions):
        yield from super().feedback(res, descriptions)
        
class SpecificTestCase(SQLUpdateTestCase):

    def wrap(self, ref_answer, student_answer, lang, msgs, test_query):
        try :
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

            cursor.executescript(sql_script)
            
            cursor.execute("SELECT title, numberOfVisitors, numberOfOnlineVisitors FROM Exhibition")
            
            self.field_names = [i[0] for i in cursor.description]
            
            res = cursor.fetchall()

            try:
                result_list = [list(row) for row in res] # Arrange result to list
                
            except IndexError as e:
                output(msgs.get_msg("UnidentifiableRecord", lang), Codes.ERROR)
                return 0, 0, None

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
       
            cursor2.executescript(ref_answer)

            cursor2.execute(test_query)
            ref = cursor2.fetchall()
            self.ref_query_result = ref
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            output(msgs.get_msg("DatabaseError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, None
        return ref, res, result_list

    def parse(self, output):
        pass
    
    def feedback(self, res, descriptions):
        yield("TooGeneralizedIdentifier", {})

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
        v.append(SpecificTestCase(
            ref_result=ref_program(),
            validator=duplicate_validator
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


def execute_test(ref_query):
    correct = False
    score = 0

    # Test category SELECT, UPDATE, DELETE, INSERT, CREATE
    test_type = "UPDATE"

    # SELECT query to test DELETE, INSERT, UPDATE, CREATE
    test_query = ("SELECT title, numberOfVisitors, numberOfOnlineVisitors "
                  "FROM Exhibition WHERE title = 'Navigating North' "
                  "AND startDate = '2022-10-07'"
                  "AND endDate = '2023-04-02'"
                  "AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma')"
                  "AND isOnlineExhibition = 1;")

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
                                    test_type,
                                    st_mname,
                                    gen_program_vector,
                                    lang, custom_msgs=msgs,
                                    insert_query=insert_query,
                                    test_query=test_query)

    correct = bool(score)
    core.set_result(correct, score)
