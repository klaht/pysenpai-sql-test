import subprocess
import json
import pytest
import yaml

def run_test_case(ans_query, ref_query):

    ans_file = "ans_file.sql"
    ref_file = "ref_file.sql"

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

def find_key_in_msgs(lang, message):
    '''Find the key of a message in the messages.yml file'''

    with open(f"../pysenpai-sql/pysenpai_sql/msg_data/{lang}/messages.yml", 'r') as f:
        data = yaml.safe_load(f)

    for _, sub_dict in data.items():
        for key, value in sub_dict.items():
            if value == message:
                return key
    return None
    

def test_success_feedback():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM Artist;"
    
    answer, msg = run_test_case(ref_query, ans_query)
    assert "CorrectResult" == find_key_in_msgs("en", msg)
    assert answer == True