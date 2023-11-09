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
