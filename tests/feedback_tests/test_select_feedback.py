from test_utils import *

def test_correct_feedback():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM Artist;"
    args = ["exNumber = 0", "show_answer_difference", "feedback=table_name, value"]

    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["CorrectResult"]

    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 1)

    assert compare_messages(returned_msgs, correct_msgs)
    assert answer

def test_incorrect_table():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM ArtWork;"

    args = ["exNumber = 0", "show_answer_difference", "feedback=table_name"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["DatabaseError"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 3)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_incorrect_column_name_SELECT():
    ans_query = "SELECT name1 FROM Artist;"
    ref_query = "SELECT name FROM Artist;"
    
    answer, output = run_test_case(ref_query, ans_query)
    returned_msgs = parse_flag_msg(output, 3)
    error_keys = ["DatabaseError"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_incorrect_column_name_WHERE():
    ans_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting');"
    ref_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting1');"
    args = ["exNumber = 0", "show_answer_difference", "feedback=table_name"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    

    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_incorrect_order():
    ans_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name DESC;"
    ref_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name ASC;"
    args = ["exNumber = 0", "feedback=table_name, order"]

    answer, output = run_test_case(ans_query, ref_query, args)

    returned_msgs = parse_flag_msg(output, 2)

    error_keys = ["incorrect_return_order", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 0)

    assert compare_messages(returned_msgs, correct_msgs)

def test_distinct():
    ans_query = "SELECT title FROM ArtWork;"
    ref_query = "SELECT DISTINCT title FROM ArtWork;"
    args = ["exNumber = 0", "show_answer_difference", "feedback=table_name, distinct"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["output_not_distinct", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer