import subprocess
import json
import pytest
import yaml
import re

def run_test_case(ans_query, ref_query):

    ans_file = "../tests/feedback_tests/ans_file.sql"
    ref_file = "../tests/feedback_tests/ref_file.sql"

    with open(ans_file, "w") as f:
        f.write(ans_query)

    with open(ref_file, "w") as f:
        f.write(ref_query)

    p = subprocess.Popen(
        ["python3", "sqlTester.py", "-l", "en", ans_file, ref_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return get_result_and_msg_from_stdout(str(p.stdout.read()))

def get_result_and_msg_from_stdout(out_str):
    copy = out_str

    out_str = str.replace(out_str, "'", "\"")
    out_str = "{" + out_str[str.find(out_str, "\"result"):]
    out_str = str.strip(out_str[:str.rfind(out_str, "}") + 1])

    msg_str = str.replace(copy, "'", "\"")
    msg_str = "{" + msg_str[str.find(msg_str, "\"msg"):]
    msg_str = msg_str[:str.find(msg_str, "}") + 1]
    
    msg_data = json.loads(msg_str)
    
    data = json.loads(out_str)

    return data['result']['correct'], msg_data["msg"]

def get_msg(lang, error):
    '''Find the message of an error key in the messages.yml file'''

    with open(f"../pysenpai-sql/pysenpai_sql/msg_data/{lang}/messages.yml", 'r') as f:
        data = yaml.safe_load(f)

    # Assuming data is structured as {lang: {error_key: message}}

    for key, value in data['program'].items():
        if error == key:  
            return value
    return None
    
def compare_messages(actual_msg, template_msg):
    '''Compare the actual message with the template message, dynamically handling variable content.'''

    actual_msg = actual_msg.replace('\n', ' ').strip()
    template_msg = template_msg.replace('\n', ' ').strip()

    if re.search(r'\{.*?\}', template_msg):
        parts = re.split(r'\{.*?\}', template_msg)
        before_var, after_var = parts[0], parts[1]

        before_var = before_var.strip()
        after_var = after_var.strip()

        # very simplified, assumes the variable is at the end of the message
        actual_msg_no_var = actual_msg[:len(before_var)]

        return (before_var + after_var) == actual_msg_no_var
    
    return actual_msg == template_msg

def test_correct_feedback():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM Artist;"
    
    answer, msg = run_test_case(ans_query, ref_query)
    correct_msg = get_msg("en", "CorrectResult")
    assert compare_messages(msg, correct_msg)
    assert answer

def test_db_error_feedback():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM Artist1;"
    
    answer, msg = run_test_case(ref_query, ans_query)
    correct_msg = get_msg("en", "DatabaseError")
    assert compare_messages(msg, correct_msg)
    assert not answer


