from test_utils import *

def test_database_error():
    ans_query = "INSERT INTO Exhibition (name, startDate, endDate, locationId, isOnlineExhibition) SELECT 'Navigating North', '2022-10-07', '2023-04-02', (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma'), 1;"
    ref_query = "INSERT INTO Exhibition (title, startDate, endDate, locationId, isOnlineExhibition) SELECT 'Navigating North', '2022-10-07', '2023-04-02', (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma'), 1;"

    args = ["exNumber = 0", "show_answer_difference", "feedback=table_name"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["DatabaseError"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 3)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_correct_feedback():
    ans_query = "INSERT INTO Exhibition (title, startDate, endDate, locationId, isOnlineExhibition) SELECT 'Navigating North', '2022-10-07', '2023-04-02', (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma'), 1;"
    ref_query = "INSERT INTO Exhibition (title, startDate, endDate, locationId, isOnlineExhibition) SELECT 'Navigating North', '2022-10-07', '2023-04-02', (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma'), 1;"
    args = ["exNumber = 0", "show_answer_difference", "feedback=table_name, value"]

    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["CorrectResult"]

    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 1)

    assert compare_messages(returned_msgs, correct_msgs)
    assert answer

def test_incorrect_insert():
    ans_query = "INSERT INTO Exhibition (title, startDate, endDate, locationId, isOnlineExhibition) SELECT 'Navigating South', '2022-10-07', '2023-04-02', (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma'), 1;"
    ref_query = "INSERT INTO Exhibition (title, startDate, endDate, locationId, isOnlineExhibition) SELECT 'Navigating North', '2022-10-07', '2023-04-02', (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma'), 1;"
    args = ["exNumber = 0", "show_answer_difference", "feedback=value"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["IncorrectInsertError", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer