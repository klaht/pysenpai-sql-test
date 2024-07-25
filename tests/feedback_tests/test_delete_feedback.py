from test_utils import *

def test_database_error():
    ans_query = "DELETE FROM Artists WHERE artistId NOT IN (SELECT artistId FROM ArtWork);"
    ref_query = "DELETE FROM Artist WHERE artistId NOT IN (SELECT artistId FROM ArtWork);"

    args = ["exNumber = 0", "show_answer_difference", "feedback=delete"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["DatabaseError"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 3)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_correct_feedback():
    ans_query = "DELETE FROM Artist WHERE artistId NOT IN (SELECT artistId FROM ArtWork);"
    ref_query = "DELETE FROM Artist WHERE artistId NOT IN (SELECT artistId FROM ArtWork);"
    args = ["exNumber = 0", "show_answer_difference", "feedback=update"]

    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["CorrectResult"]

    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 1)

    assert compare_messages(returned_msgs, correct_msgs)
    assert answer

def test_too_many_deleted():
    ans_query = "DELETE FROM Artist WHERE artistId != 1;"
    ref_query = "DELETE FROM Artist WHERE artistId NOT IN (SELECT artistId FROM ArtWork);"

    args = ["exNumber = 0", "show_answer_difference", "feedback=delete"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["tooManyDeleted", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 2)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_too_few_deleted():
    ans_query = "DELETE FROM Artist WHERE artistId = 1;"
    ref_query = "DELETE FROM Artist WHERE artistId NOT IN (SELECT artistId FROM ArtWork);"

    args = ["exNumber = 0", "show_answer_difference", "feedback=delete"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["tooFewDeleted", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 2)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_incorrect_delete():
    ans_query = "DELETE FROM Artist WHERE artistId = 2;"
    ref_query = "DELETE FROM Artist WHERE artistId = 1;"

    args = ["exNumber = 0", "show_answer_difference", "feedback=delete"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["incorrectDeletedRows", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 2)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer