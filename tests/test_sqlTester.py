import subprocess
import json
import os
import pytest

def test_update():
    run_tests_from_directory("../tests/update_test_files")

def test_select():
    run_tests_from_directory("../tests/select_test_files")

def test_create():
    run_tests_from_directory("../tests/create_test_files")

def test_delete():
    run_tests_from_directory("../tests/delete_test_files")

def test_alter():
    run_tests_from_directory("../tests/alter_test_files")

def test_insert():
    run_tests_from_directory("../tests/insert_test_files")

def test_multiline():
    run_tests_from_directory("../tests/multiple_query_test_files")

@pytest.mark.fuzz
def test_fuzz():
    '''
    Runs the input in fuzz_input.txt file line by line against the ref.sql file.
    Used for testing fuzz inputs. 
    Is ran with --fuzz flag, so it is not ran by default (pytest -m --fuzz)
    '''
    run_fuzz("../tests/fuzz_test_files/case1/fuzz_input.txt", "../tests/fuzz_test_files/case1/ref.sql")

def run_fuzz(input_list, ref_file):
    msg_list = ["Your answer is empty.", "No valid SQL command detected.", "The input contains invalid characters."]

    with open(input_list, "r", encoding='utf-8') as f:
        fuzz_strings = f.readlines()
    for i, s in enumerate(fuzz_strings):
        if s.startswith("#"): # Skip commented lines
            continue
        
        with open("fuzz_string.sql", "w", encoding='utf-8') as sql_file:
            sql_file.write(s)

        print(f"Running test case {i + 1} of {len(fuzz_strings)}")
        # Run the test case with the fuzz string
        answer, msg = run_test_case(ref_file, "fuzz_string.sql", True)
        assert answer == False # Should always be false, as the fuzz string should not pass the test
        assert msg in msg_list # Check that the error message is one of the expected ones
        # Clear the file by reopening it in write mode
        open("fuzz_string.sql", "w").close()

def run_tests_from_directory(dir):
    for test_case in open_root_directory(dir):
        test_file_path, ref_file_path, should_pass = test_case
        assert should_pass == run_test_case(test_file_path, ref_file_path)

def run_test_case(ans_file, ref_file, msg=False):
    p = subprocess.Popen(
        ["python3", "sqlTester.py", "-l", "en", ans_file, ref_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    if msg:
        return get_result_and_msg_from_stdout(str(p.stdout.read()))
    
    return get_result_from_stdout(str(p.stdout.read()))

def get_result_from_stdout(out_str):

    out_str = str.replace(out_str, "'", "\"")
    out_str = "{" + out_str[str.find(out_str, "\"result"):]
    out_str = str.strip(out_str[:str.rfind(out_str, "}") + 1])

    data = json.loads(out_str)

    return data['result']['correct']

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

def open_root_directory(path):
    test_cases = []
    for dir in os.listdir(path):
        for file in os.listdir(path + "/" + dir):
            #Skip reference file
            if file == "ref.sql":
                continue

            test_cases.append([
                    path + "/" + dir + "/" + file, 
                    path + "/" + dir + "/ref.sql", 
                    str.startswith(file, "pass_")
            ])

    return test_cases
            