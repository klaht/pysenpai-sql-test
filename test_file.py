import importlib
import re
import sqlite3
import pysenpai.core as core
from pysenpai.messages import Codes

import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import json_output
from pysenpai.messages import load_messages, Codes
from pysenpai.output import output

import re
import pysenpai.core as core
from pysenpai.messages import Codes
import pysenpai.utils.checker as utils
from pysenpai.exceptions import OutputParseError

#Temporary raw test file that has all dependencies included in the file itself

import importlib
import io
import sqlite3
import sys

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import json_output
from pysenpai.messages import load_messages, Codes
from pysenpai.output import output

class SQLTestCase(object):
    
    def __init__(self, ref_result, 
                 args=None,
                 inputs=None,
                 data=None,
                 weight=1,
                 tag="",
                 validator=defaults.result_validator,
                 output_validator=None,
                 eref_results=None,
                 internal_config=None,
                 presenters=None):
                 
        self.args = args or []
        self.inputs = inputs or []
        self.data = data
        self.weight = weight
        self.tag = tag
        self.ref_result = ref_result
        self.validator = validator
        self.output_validator = output_validator
        self.eref_results = eref_results or []
        self.correct = False
        self.output_correct = False
        self.internal_config = internal_config
        self.presenters = {
            "arg": defaults.default_value_presenter,
            "input": defaults.default_input_presenter,
            "data": defaults.default_value_presenter,
            "ref": defaults.default_value_presenter,
            "res": defaults.default_value_presenter,
            "parsed": defaults.default_value_presenter,
            "call": defaults.default_call_presenter
        }
        if presenters:
            self.presenters.update(presenters)
    
    def configure_presenters(self, patch):
        self.presenters.update(patch)
    
    def present_object(self, category, value):
        return self.presenters[category](value)
        
    def present_call(self, target):
        return ""
    
    def feedback(self, res, descriptions):
        for eref_result, msg_key in self.eref_results:
            try:
                self.validator(eref_result, res, descriptions)
                yield (msg_key, {})
            except AssertionError:
                pass

    def parse(self, output):
        return output
    
    def validate_result(self, res, parsed, output):
        self.validator(self.ref_result, res, parsed)
        self.correct = True
    
    def validate_output(self, output):
        self.output_validator(output, self.args, self.inputs)
        self.output_correct = True
    
    def wrap(self, module, target):
        raise NotImplementedError

    def teardown(self):
        pass

class SQLQueryTestCase(SQLTestCase):
    
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
                 presenters=None):
        
        super().__init__(
            ref_result, args, inputs, data, weight, tag, validator, output_validator, eref_results, internal_config, presenters
        )

    def wrap(self, module, target):
        importlib.reload(module)

def run_sql_test_cases(category, test_category, test_target, test_cases, lang,
                  test_query=None,
                  insert_query=None, 
                  parent_object=None,
                  msg_module="pysenpai",
                  custom_msgs={},
                  hide_output=True,
                  test_recurrence=True,
                  validate_exception=False,
                  argument_cloner=defaults.default_argument_cloner,
                  new_test=defaults.default_new_test,
                  grader=defaults.pass_fail_grader): 

    # One time preparations
    save = sys.stdout
    msgs = load_messages(lang, category, module=msg_module)
    msgs.update(custom_msgs)
    
    # call test and input producing functions 

    # if inspect.isfunction(test_cases):
    test_cases = test_cases()
    
    # Show the name of the function
    json_output.new_test(
        msgs.get_msg("TargetName", lang)["content"].format(name=test_target)
    )

    for i, test in enumerate(test_cases):
      
        json_output.new_run()

        if test.args:
            output(
                msgs.get_msg("PrintTestVector", lang), Codes.DEBUG,
                args=test.present_object("arg", test.args),
                call=test.present_call(test_target)
            )
        if test.inputs:
            output(
                msgs.get_msg("PrintInputVector", lang), Codes.DEBUG,
                inputs=test.present_object("input", test.inputs)
            )
        if test.data:
            output(
                msgs.get_msg("PrintTestData", lang), Codes.DEBUG,
                data=test.present_object("data", test.data)
            )
    
        match test_category:
            case "SELECT":
                ref, res, column_names = select_test(test.ref_result, test_target, lang, msgs)
                if (ref == 0 or res == 0):
                    return 0

            case "INSERT" | "UPDATE" | "DELETE":
                ref, res = insert_update_test(test.ref_result, test_target, lang, msgs, test_query=test_query)
                if (ref == 0 or res == 0):
                    return 0

            case "CREATE":
                ref, res = create_test(test.ref_result, test_target, lang, msgs, test_query=test_query, insert_query=insert_query)
                if (ref == 0 or res == 0):
                    return 0
            case _:
                output(msgs.get_msg("PrintStudentOutput", lang), Codes.INFO)
                return 0
        # Test preparations


        # Validating function results
        sys.stdout = save
        if not hide_output:
            output(msgs.get_msg("PrintStudentOutput", lang), Codes.INFO)
        
        # Validate results
        try: 
            
            test.validate_result(res, ref, None)           
            output(msgs.get_msg("CorrectResult", lang), Codes.CORRECT)
        except AssertionError as e:
            # Result was incorrect
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            output(
                msgs.get_msg("PrintReference", lang),
                Codes.DEBUG,
                ref=test.present_object("ref", test.ref_result)
            )

            output(msgs.get_msg("AdditionalTests", lang), Codes.INFO)
                
            #Extra feedback
            if column_names != None:
                for msg_key, format_args in test.feedback(res, column_names):
                    output(msgs.get_msg(msg_key, lang), Codes.INFO, **format_args)
        
        test.teardown()
        prev_res = res
        prev_out = test_cases
    
    return grader(test_cases)

def insert_update_test(ref_answer, student_answer, lang, msgs, test_query):

        # Run student and reference querys and return answers
        # Insert and update are both tested with this

        # Open student answer
        try :
            sql_file = open(student_answer, 'r')
            sql_script = sql_file.read()
        except FileNotFoundError as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0,0

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
       
            cursor.executescript(sql_script)
        
            cursor.execute(test_query)
            
            res = cursor.fetchall()

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0, 0
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
       
            cursor2.executescript(ref_answer)

            cursor2.execute(test_query)
            ref = cursor2.fetchall()
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            print(str(e))
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0, 0
        
        return ref, res


def select_test(ref_answer, student_answer, lang, msgs):
     
     # Run student and reference querys and return answers
    
        # Open student answer
        try :
            sql_file = open(student_answer, 'r')
     
            sql_script = sql_file.read()
        except FileNotFoundError as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0,0

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
       
            cursor.execute(sql_script)
            res = cursor.fetchall()
        
            column_names = [description[0] for description in cursor.description]

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0,0
        
        # Run reference answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
       
            cursor.execute(ref_answer)
            ref = cursor.fetchall()
        
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0,0

        return ref, res, column_names

def create_test(ref_answer, student_answer, lang, msgs, test_query, insert_query):

        # Run student and reference querys and return answers
        # Insert and update are both tested with this

        # Open student answer
        try :
            sql_file = open(student_answer, 'r')
            sql_script = sql_file.read()
        except FileNotFoundError as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0,0

        # Run student answer
        try: 
            conn = sqlite3.connect("mydatabase1.db")
            cursor = conn.cursor()
            
            cursor.executescript(sql_script)
            
            # Insert to created table
            cursor.executescript(insert_query)
        
            cursor.execute(test_query)
            
            res = cursor.fetchall()

            conn.commit()
            cursor.close()
            conn.close()
           
        except sqlite3.Error as e:
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0, 0
        
        # Run reference answer
        try: 
            conn2 = sqlite3.connect("mydatabase2.db")
            cursor2 = conn2.cursor()
       
            cursor2.executescript(ref_answer)

            # Insert to created table
            cursor2.executescript(insert_query)

            cursor2.execute(test_query)
            ref = cursor2.fetchall()
        
            conn2.commit()
            cursor2.close()
            conn2.close()

        except sqlite3.Error as e:
            print(str(e))
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            return 0, 0
        
        return ref, res


import io
import os.path
import sys
import pysenpai.callbacks.defaults as defaults
from pysenpai.output import json_output
from pysenpai.messages import load_messages, Codes 
from pysenpai.output import output
from pysenpai.utils.internal import FNAME_PAT


def load_sql_module(
                module_path, 
                lang="en", 
                custom_msgs={}, 
                inputs=[],
                hide_output=True, 
                allow_output=True, 
                presenter=defaults.default_input_presenter):
    """
    load_module(module_path[, lang="en"][, custom_msgs={}][, inputs=[]][, hide_output=True][, allow_output=True][, presenter=default_input_presenter]) -> Module
    
    This function imports the student module and needs to be called before doing tests.
    The parameters are
    
    * *lang* - language for messages
    * *custom_msgs* - a TranslationDict object that includes additions/overrides 
      to the default import messages
    * *inputs* - input vector to be given to the program; inputs are automatically joined 
      by newlines and made into a StringIO object that replaces standard input. When 
      calling this function you need to provide inputs that allow the program to execute
      without errors. 
    * *hide_output* - a flag to hide or show output, by default output is hidden
    * *allow_output* - a flag that dictates whether it's considered an error if the code
      has output or not. By default output is allowed.
    * *presenter* - a presenter function for showing inputs in the output in case of
      errors
       
    Before attempting to import the student module, the function checks whether the 
    filename is a proper Python module name. None is returned if the filename is
    invalid. This also happens if the module has the same name as a Python library module.
    
    If importing the student module results in an exception, the exception's name is
    looked up from the message dictionary and the corresponding error message is
    shown in the checker output. If the exception name is not found, GenericErrorMsg
    is shown instead. See :ref:`Output Messages <output-messages>` for information
    about how to specify your own error messages. 
    
    If importing is successful and *allow_output* is set to False, the StringOutput
    object is checked for prints and an error message is given if content is found.
    Otherwise the module object is returned.    
    """

    save = sys.stdout
    msgs = load_messages(lang, "import")
    msgs.update(custom_msgs)
    module_name = os.path.basename(module_path)
    
    json_output.new_test(msgs.get_msg("LoadingModule", lang)["content"].format(name=module_name))
    json_output.new_run()
    
    if not module_name.endswith(".sql"):
        output(msgs.get_msg("MissingFileExtension", lang), Codes.ERROR)
        print("MissingFileExtension")
        return None
    
    name = module_name.rsplit(".sql", 1)[0]
    
    if not FNAME_PAT.fullmatch(name):    
        output(msgs.get_msg("BadModuleName", lang), Codes.ERROR, name=module_name)
        print("BadModuleName")
        return None
        
    pyver = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
        
    if name in sys.stdlib_module_names:
        output(msgs.get_msg("SystemModuleName", lang), Codes.ERROR, name=module_name)
        print("SystemModuleName")
        return None
   
    if inputs:
        sys.stdin = io.StringIO("\n".join([str(i) for i in inputs]))


msgs = core.TranslationDict()
float_pat = re.compile("(-?[0-9]+\.[0-9]+)")

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

def parsed_list_sql_validator(ref, res, out):
    """
    This is a convenience callback for validating lists of parsed results against 
    a reference list. The comparison of out to ref is done item by item as opposed 
    to the default validator (which compares res). Comparison is done item to item.
    """

    try:
        for i, v in enumerate(res):
            assert v == out[i], "fail_output_result"
    except IndexError:
        raise AssertionError
    
    
msgs = core.TranslationDict()
float_pat = re.compile("(-?[0-9]+\.[0-9]+)")

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

            descriptions = [item.lower() for item in descriptions] # convert to lowercase

            incorrect_variables = descriptions != correct
            incorrect_order = sorted(descriptions) == sorted(correct) and incorrect_variables

            if incorrect_order:
                yield ("incorrect_column_order", {})
            elif incorrect_variables:
                yield ("incorrect_selected_columns", {})

        except AssertionError:
            pass

def gen_program_vector():
    v = []
    for i in range(1):
        v.append(MainTestCase(
            ref_result=ref_program(),
            validator=parsed_list_sql_validator
        ))
    return v

def ref_program():
    correct_answer = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, name VARCHAR (50) NOT NULL);"
    return correct_answer

if __name__ == "__main__":
    correct = False
    score = 0

    # Test category SELECT, UPDATE, DELETE, INSERT, CREATE
    test_type = "CREATE"
    
    # SELECT query to test DELETE, INSERT, UPDATE, CREATE
    test_query = "SELECT * FROM testtable"
    
    # INSERT query to test CREATE
    insert_query = "INSERT INTO testtable VALUES (1, 'testi')"


    core.init_test(__file__, 1)
    
    msgs.update(msgs)

    files, lang = core.parse_command()

    st_mname = files[0]

    st_module = load_sql_module(st_mname, lang, inputs=["0"])

    score += run_sql_test_cases("program", test_type, st_mname, gen_program_vector, lang, custom_msgs=msgs, insert_query=insert_query, test_query=test_query)

    correct = bool(score)
    core.set_result(correct, score)
