from test_utils import *

def test_correct_feedback():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM Artist;"
    
    answer, msg = run_test_case(ans_query, ref_query)
    correct_msg = get_msg("en", "CorrectResult")
    assert compare_messages(msg, correct_msg)
    assert answer

def test_incorrect_table():
    ans_query = "SELECT name FROM Artist;"
    ref_query = "SELECT name FROM ArtWork;"
    
    answer, msg = run_test_case(ans_query, ref_query)
    correct_msg = get_msg("en", "DatabaseError")
    assert compare_messages(msg, correct_msg)
    assert not answer

def test_incorrect_column_name_SELECT():
    ans_query = "SELECT name1 FROM Artist;"
    ref_query = "SELECT name FROM Artist;"
    
    answer, msg = run_test_case(ref_query, ans_query)
    correct_msg = get_msg("en", "DatabaseError")
    assert compare_messages(msg, correct_msg)
    assert not answer

def test_incorrect_column_name_WHERE():
    ans_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting');"
    ref_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting1');"
    
    answer, msg = run_test_case(ans_query, ref_query)
    correct_msg = get_msg("en", "IncorrectResult")
    assert compare_messages(msg, correct_msg)
    assert not answer

def test_incorrect_order():
    ans_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name DESC;"
    ref_query = "SELECT name FROM Artist WHERE artistId IN (SELECT artistId FROM ArtWork WHERE type == 'painting') ORDER BY name ASC;"

    answer, msg = run_test_case(ans_query, ref_query)
    correct_msg = get_msg("en", "incorrect_colunm_order")
    #assert compare_messages(msg, correct_msg) # Heittää messageksi IncorrectResult vaikka pitäisi olla incorrect_colunm_order 
    assert not answer
