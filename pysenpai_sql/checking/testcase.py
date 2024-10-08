import importlib
import io
import sqlite3
import sys

import pysenpai.callbacks.defaults as defaults
import pysenpai.callbacks.convenience as convenience
from pysenpai.output import json_output
from pysenpai_sql.messages import load_messages, Codes
from pysenpai.output import output
from pysenpai_sql.checking.tests import *

def get_assignment_type_output_msg(ref_query:str) -> str:
    assignmentType = ref_query.split()[0]
    match assignmentType.upper():
        case "SELECT":
            return "selectOutput"
        case "INSERT":
            return "insertOutput"
        case "UPDATE":
            return "updateOutput"
        case "DELETE":
            return "deleteOutput"

    return "PrintStudentOutput"

class SQLTestCase(object):
    
    def __init__(self, ref_result,
                 res_result=None, 
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
        self.res_result = res_result
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
        self.feedback_params = {}
    
    def configure_presenters(self, patch):
        self.presenters.update(patch)
    
    def present_object(self, category, value):
        return self.presenters[category](value)
        
    def present_call(self, target):
        return ""
    
    def feedback(self, res, ref, config_file):
        feedback_results = []
        for setting in open(config_file, "r").readlines():
            if setting.find("feedback") >= 0:
                parsed_functions = setting.split("=")[1].split(",")
                self.feedback_params['ref'] = self.ref_result
                self.feedback_params['res'] = self.res_result
                for function in parsed_functions:
                    try:
                        feedback_results.append(feedback_functions[function.strip()](res, ref, feedback_params=self.feedback_params)) #Call feedback function
                    except KeyError:
                        # TODO: Contact course staff without displaying error? Could be typo in config etc
                        pass
            
                return feedback_results

        return [(None, None)]

    def parse(self, output):
        return output
    
    def validate_result(self, res, parsed, output):
        self.validator(self.ref_result, res, parsed)
        self.correct = True
    
    def validate_output(self, output):
        self.output_validator(output, self.args, self.inputs)
        self.output_correct = True
    
    def wrap(self, ref_answer, student_answer, lang, msgs, test_query, insert_query):
        raise NotImplementedError

    def teardown(self):
        pass

def run_sql_test_cases(category, test_category, test_target, test_cases, lang,
                  res_result=None,
                  test_query=None,
                  insert_query=None, 
                  parent_object=None,
                  msg_module="pysenpai_sql",
                  custom_msgs={},
                  hide_output=True,
                  test_recurrence=True,
                  validate_exception=False,
                  argument_cloner=defaults.default_argument_cloner,
                  new_test=defaults.default_new_test,
                  grader=defaults.pass_fail_grader,
                  config_file="setting_arguments.txt"): 

    # One time preparations
    save = sys.stdout
    msgs = load_messages(lang, category, module=msg_module)
    
    # call test and input producing functions 

    # if inspect.isfunction(test_cases):
    test_cases = test_cases()
    
    # Show the name of the function
    json_output.new_test(
        msgs.get_msg("TargetName", lang)["content"].format(name=test_target)
    )

    for i, test in enumerate(test_cases):
      
        json_output.new_run()

        column_names = None

        try:
            inps = test.inputs
            sys.stdin = io.StringIO("\n".join([str(x) for x in inps]))
        except IndexError:
            inps = []

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
    
            
        #Open student answer file
        try :
            sql_file = open(test_target, 'r')
            student_answer = sql_file.read()
        except FileNotFoundError as e:
            output(msgs.get_msg("FileOpenError", lang), Codes.ERROR, emsg=str(e))
            return 0, 0, ""
        
        student_answer = student_answer.replace('\n', ' ')
        if not student_answer.strip().endswith(';'):
            output(msgs.get_msg("missingSemicolon", lang), Codes.INCORRECT)
            return 0


        #Run test
        ref, res = test.wrap(test.ref_result, student_answer, lang, msgs)
        if (ref == 0 or res == 0):
            #Don't print output as zero, could be confusing for the student
            #output(msgs.get_msg("PrintStudentOutput", lang), Codes.INFO, output=res)
            return 0

        # Validating function results
        sys.stdout = save
        if not hide_output:
            output(msgs.get_msg("PrintStudentOutput", lang), Codes.INFO, None)
        
        # Validate results
        try: 
            test.validate_result(res, ref, None)           
            output(msgs.get_msg("CorrectResult", lang), Codes.CORRECT)
        except AssertionError as e:
            # Result was incorrect
            output(msgs.get_msg(e, lang, "IncorrectResult"), Codes.INCORRECT)
            for setting in open(config_file, "r").readlines():
                if setting.find("show_reference") >= 0:
                    output(
                        msgs.get_msg("PrintReference", lang),
                        Codes.DEBUG,
                        ref=test.present_object("ref", ref)
                    )

                if setting.find("show_output") >= 0:
                    output(
                        msgs.get_msg(
                            get_assignment_type_output_msg(student_answer), 
                            lang
                        ),
                        Codes.DEBUG,
                        output=test.present_object("parsed", res)
                    )

            #Extra feedback
            printed_additional_test_message = False
            for msg_key, test_output in test.feedback(res, ref, config_file):
                '''Only print additional tests message if there are messages to display'''
                if not printed_additional_test_message and msg_key:
                    output(msgs.get_msg("AdditionalTests", lang), Codes.INFO)
                    printed_additional_test_message = True

                if test_output == None and msg_key:
                    output(msgs.get_msg(msg_key, lang), Codes.INFO)
                elif msg_key:
                    output(msgs.get_msg(msg_key, lang), Codes.INFO, output=test_output)
                
        test.teardown()
    
    return grader(test_cases)

