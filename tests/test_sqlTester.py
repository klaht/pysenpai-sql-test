import subprocess
import json
import os


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

def run_tests_from_directory(dir):
    for test_case in open_root_directory(dir):
        test_file_path, ref_file_path, should_pass = test_case
        assert should_pass == run_test_case(test_file_path, ref_file_path)

def run_test_case(ans_file, ref_file):
    p = subprocess.Popen(
        ["python3", "sqlTester.py", "-l", "fi", ans_file, ref_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return get_result_from_stdout(str(p.stdout.read()))

def get_result_from_stdout(out_str):
    out_str = str.replace(out_str, "'", "\"")
    out_str = "{" + out_str[str.find(out_str, "\"result"):]
    out_str = str.strip(out_str[:str.rfind(out_str, "}") + 1])
    data = json.loads(out_str)


    return data['result']['correct']

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
            