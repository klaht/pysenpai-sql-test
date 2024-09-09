import subprocess
import json
import pytest
import yaml
import re

def run_test_case(ans_query, ref_query, args=[], flag=0):

    ans_file = "../tests/feedback_tests/ans_file.sql"
    ref_file = "../tests/feedback_tests/ref_file.sql"

    with open(ans_file, "w") as f:
        f.write(ans_query)

    with open(ref_file, "w") as f:
        f.write(ref_query)
    
    with open("test_setting_arguments.txt", "w") as f:
        f.write("\n".join(args))

    p = subprocess.Popen(
        ["python3", "sqlTester.py", "-l", "en", ans_file, ref_file, "test_setting_arguments.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    return get_result_and_msg_from_stdout(str(p.stdout.read()))

def get_result_and_msg_from_stdout(out_str):
    copy = out_str

    out_str = str.replace(out_str, "'", "\"")
    out_str = "{" + out_str[str.find(out_str, "\"result"):]
    out_str = str.strip(out_str[:str.rfind(out_str, "}") + 1])

    data = json.loads(out_str)

    return (data['result']['correct'], copy)

def parse_flag_msg(out_str, flag):
    msg_str = str.replace(out_str, "'", "\"")
    msg_str = "{" + msg_str[str.find(msg_str, "\"tests"):]
    msg_str = str.strip(msg_str[:str.rfind(msg_str, "}") + 1])

    msg_data = json.loads(msg_str)

    messages = []

    # parse the output to find all output messages
    for test in msg_data['tests']:
        if test['title'] == "Testing program...":
            for run in test['runs']:
                for message in run['output']:
                    if message['flag'] == flag:
                        messages.append(message['msg'])
    #print("messages:",messages)
    return messages

def get_msg(lang, error_keys):
    '''Find the message of an error key in the messages.yml file'''

    with open(f"../pysenpai_sql/msg_data/{lang}/messages.yml", 'r') as f:
        data = yaml.safe_load(f)

    keys = []

    for error_key in error_keys:
        for key, value in data['program'].items():
            if error_key == key: 
                keys.append(value)
    return keys
    
def compare_messages(actual_msgs, template_msgs):
    '''Compare the actual message with the template message, ensuring all template messages are found in actual messages.'''

    if (len(actual_msgs) == 0) or (len(template_msgs) == 0):
        return False

    # Normalize and prepare template messages for comparison
    normalized_template_msgs = [msg.replace('"', "'").replace('\n', ' ').replace('\\n', ' ' ).strip() for msg in template_msgs]

    # Normalize actual messages
    normalized_actual_msgs = [msg.replace('"', "'").replace('\n', ' ').replace('\\n', ' ' ).strip() for msg in actual_msgs]

    # Check each template message against actual messages
    for template_msg in normalized_template_msgs:
        # Initialize a flag to check if the current template message is found
        template_msg_found = False

        # Check if the template message contains a variable placeholder
        if re.search(r'\{.*?\}', template_msg):
            parts = re.split(r'\{.*?\}', template_msg)
            if len(parts) >= 2:
                before_var, after_var = parts[0].strip(), parts[1].strip()

                # Check each actual message to see if it matches the template
                for actual_msg in normalized_actual_msgs:
                    # Check if the actual message matches the start and end of the template message
                    if actual_msg.startswith(before_var) and actual_msg.endswith(after_var):
                        template_msg_found = True
                        break
        else:
            # If the template message does not contain a variable placeholder, check for direct presence
            if template_msg in normalized_actual_msgs:
                template_msg_found = True

        # If the current template message was not found in any actual message
        if not template_msg_found:
            return False

    # If all template messages have been found in actual messages
    return True