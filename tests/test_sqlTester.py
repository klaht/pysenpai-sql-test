import pytest
import subprocess
import json
import os

def run_test_case(ans_file, ref_file):
    p = subprocess.Popen(
        ["python3", "sqlTester.py", "-l", "fi", ans_file, ref_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return get_result_from_stdout(str(p.stdout.read()))

def get_result_from_stdout(out_str):
    print(out_str)
    out_str = "{" + out_str[str.find(out_str, "result") - 1:]
    out_str = str.strip(out_str[:str.rfind(out_str, "}") + 1])
    data = json.loads(out_str)

    print(data)

    return data['result']['correct']

def test_update():
    for test_case in open_root_directory("../tests/update_test_files"):
        test_file_path, ref_file_path, should_pass = test_case
        assert run_test_case(test_file_path, ref_file_path) == should_pass

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
            