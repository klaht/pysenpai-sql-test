from test_utils import *

def test_database_error():
    ans_query = "UPDATE exhibition SET numberOfVisitorsWrong = 14000, numberOfOnlineVisitors = 50000 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"
    ref_query = "UPDATE exhibition SET numberOfVisitors = 14000, numberOfOnlineVisitors = 50000 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"

    args = ["exNumber = 0", "show_answer_difference", "feedback=update"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["DatabaseError"]
    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 3)

    assert compare_messages(returned_msgs, correct_msgs)
    assert not answer

def test_correct_feedback():
    ans_query = "UPDATE exhibition SET numberOfVisitors = 14000, numberOfOnlineVisitors = 50000 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"
    ref_query = "UPDATE exhibition SET numberOfVisitors = 14000, numberOfOnlineVisitors = 50000 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"
    args = ["exNumber = 0", "show_answer_difference", "feedback=update"]

    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["CorrectResult"]

    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 1)

    assert compare_messages(returned_msgs, correct_msgs)
    assert answer

def test_incorrect_update_where():
    ans_query = "UPDATE exhibition SET numberOfVisitors = 14000, numberOfOnlineVisitors = 50000 WHERE startDate = '2022-10-07'"
    ref_query = "UPDATE exhibition SET numberOfVisitors = 14000, numberOfOnlineVisitors = 50000 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"

    args = ["exNumber = 0", "show_answer_difference", "feedback=update"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectSelectedRows", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_updated_values():
    ans_query = "UPDATE exhibition SET numberOfVisitors = 15000, numberOfOnlineVisitors = 2 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"
    ref_query = "UPDATE exhibition SET numberOfVisitors = 14000, numberOfOnlineVisitors = 50000 WHERE title = 'Navigating North' AND startDate = '2022-10-07' AND endDate = '2023-04-02' AND locationId = (SELECT locationId FROM location WHERE name = 'Museum of Contemporary Art Kiasma') AND isOnlineExhibition = 1;"

    args = ["exNumber = 0", "show_answer_difference", "feedback=update"]
    
    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectUpdatedValues", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_different_update_format():
    ref_query = """
        UPDATE Artwork
        SET collectionId = (SELECT collectionId FROM Collection WHERE name = 'Collection of the Oulu Museum of Art')
        WHERE title = 'La Merenda' 
        AND artistId = (SELECT artistId FROM Artist WHERE name = 'Elin Danielson-Gambogi' AND yearBorn = 1861)
        AND year = 1904
        AND type = 'painting'
        AND material = 'oil on canvas';
    """
    ans_query = """
        UPDATE Artwork
        SET collectionId = (SELECT collectionId FROM Collection WHERE name = 'Collection of the Oulu Museum of Art')
        WHERE title = 'La Merenda' 
        AND artistId = (SELECT artistId FROM Artist WHERE name = 'Elin Danielson-Gambogi' AND yearBorn = 1861)
        AND year = 1904
        AND type = 'painting'
        AND material = 'oil on canvas';
    """

    args = ["exNumber = 0", "show_answer_difference", "feedback=update"]

    answer, output = run_test_case(ans_query, ref_query, args)
    error_keys = ["CorrectResult"]

    correct_msgs = get_msg("en", error_keys)
    returned_msgs = parse_flag_msg(output, 1)

    assert compare_messages(returned_msgs, correct_msgs)
    assert answer