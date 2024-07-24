from test_utils import *

def test_correct_feedback():
    ans_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age VARCHAR (50) NOT NULL);"
    ref_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age VARCHAR (50) NOT NULL);"
    args = ["exNumber = 0", "show_answer_difference", "feedback=schema"]

    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["CorrectResult"]

    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 1)

    assert compare_messages(returned_msgs, correct_msgs)
    assert answer

def test_incorrect_table_name():
    ans_query = "CREATE TABLE test (Id INTEGER PRIMARY KEY, age VARCHAR (50) NOT NULL);"
    ref_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age VARCHAR (50) NOT NULL);"

    args = ["exNumber = 0", "show_answer_difference", "feedback=schema"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectTableName", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_column_name():
    ans_query = "CREATE TABLE testtable (IdWrong INTEGER PRIMARY KEY, age VARCHAR (50) NOT NULL);"
    ref_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age VARCHAR (50) NOT NULL);"

    args = ["exNumber = 0", "show_answer_difference", "feedback=schema"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectColumnName", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_data_type():
    ans_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age INTEGER NOT NULL, name INTEGER);"
    ref_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age INTEGER NOT NULL, name VARCHAR (50));"

    args = ["exNumber = 0", "show_answer_difference", "feedback=schema"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectDataType", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_not_null():
    ans_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age INTEGER, name VARCHAR(50));"
    ref_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age INTEGER NOT NULL, name VARCHAR( 50));"

    args = ["exNumber = 0", "show_answer_difference", "feedback=schema"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectNotNull", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_primary_key():
    ans_query = "CREATE TABLE testtable (Id INTEGER, age INTEGER NOT NULL PRIMARY KEY, name VARCHAR(50));"
    ref_query = "CREATE TABLE testtable (Id INTEGER PRIMARY KEY, age INTEGER NOT NULL, name VARCHAR( 50));"

    args = ["exNumber = 0", "show_answer_difference", "feedback=schema"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectPrimaryKey", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer