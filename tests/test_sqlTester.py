import pytest
import subprocess
import unittest
import json

def run_test_case(ans_file, ref_file):
    p = subprocess.Popen(
        ["python3", "sqlTester.py", "-l", "fi", ans_file, ref_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return get_result_from_stdout(str(p.stdout.read()))

def get_result_from_stdout(out_str):
    out_str = "{" + out_str[str.find(out_str, "result") - 1:]
    out_str = str.strip(out_str[:str.rfind(out_str, "}") + 1])
    data = json.loads(out_str)

    return data['result']['correct']



    
def test_update():
    assert run_test_case("answer.sql", "reference.sql")
