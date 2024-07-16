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

    error_keys = ["incorrectReturnOrder", "AdditionalTests"]
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
    error_keys = ["noDistinctKeyword", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_no_group_by():
    ans_query = """
        SELECT name FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID  
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionid  
        ORDER BY name ASC; 
    """
    ref_query = """
        SELECT name FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID  
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionid  
        GROUP BY name HAVING MIN(on_exhibition.numberoflikes) > 0 
        ORDER BY name ASC; 
    """
    args = ["exNumber = 0", "show_answer_difference", "feedback=group_by"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["noGroupByKeyword", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_group_by():
    ans_query = """
        SELECT name FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID  
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionid  
        GROUP BY on_exhibition.exhibitionID HAVING MIN(on_exhibition.numberoflikes) > 0 
        ORDER BY name ASC; 
    """
    ref_query = """
        SELECT name FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID  
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionid  
        GROUP BY name HAVING MIN(on_exhibition.numberoflikes) > 0 
        ORDER BY name ASC; 
    """
    args = ["exNumber = 0", "show_answer_difference", "feedback=group_by"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectGroupBy", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_no_having():
    ans_query = """
        SELECT exhibition.title, artist.name, numberofvisitors 
        FROM on_exhibition, artwork, artist, exhibition 
        WHERE on_exhibition.exhibitionid = exhibition.exhibitionid 
        AND on_exhibition.artworkid = artwork.artworkid 
        AND artwork.artistid = artist.artistid 
        GROUP BY exhibition.exhibitionid 
        ORDER BY exhibition.title;
    """
    ref_query = """
        SELECT exhibition.title, artist.name, numberofvisitors 
        FROM on_exhibition, artwork, artist, exhibition 
        WHERE on_exhibition.exhibitionid = exhibition.exhibitionid 
        AND on_exhibition.artworkid = artwork.artworkid 
        AND artwork.artistid = artist.artistid 
        GROUP BY exhibition.exhibitionid 
        HAVING COUNT(artwork.artistid) < 4 
        ORDER BY exhibition.title;
    """
    args = ["exNumber = 0", "show_answer_difference", "feedback=group_by"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["noHavingKeyword", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_having():
    ans_query = """
        SELECT name FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID  
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionid  
        GROUP BY name HAVING MAX(on_exhibition.numberoflikes) = 2
        ORDER BY name ASC; 
    """
    ref_query = """
        SELECT name FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID  
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionid  
        GROUP BY name HAVING MIN(on_exhibition.numberoflikes) > 0 
        ORDER BY name ASC; 
    """
    args = ["exNumber = 0", "show_answer_difference", "feedback=group_by"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectHavingKeyword", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_missing_join():
    ans_query = """
        SELECT DISTINCT artist.name, exhibition.title FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID 
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionID 
        ORDER BY artist.name ASC, exhibition.title ASC; 
    """
    ref_query = """
        SELECT DISTINCT artist.name, exhibition.title, location.city FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID 
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionID 
        JOIN location ON exhibition.locationID = location.locationID 
        WHERE artist.birthplace = location.city 
        ORDER BY artist.name ASC, exhibition.title ASC; 
    """
    args = ["exNumber = 0", "show_answer_difference", "feedback=join"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["tableNotJoined", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer

def test_incorrect_join():
    ans_query = """
        SELECT DISTINCT artist.name, exhibition.title, location.city FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID 
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionID 
        JOIN location ON exhibition.title = location.city 
        ORDER BY artist.name ASC, exhibition.title ASC; 
    """
    ref_query = """
        SELECT DISTINCT artist.name, exhibition.title, location.city FROM artist 
        JOIN artwork ON artist.artistID = artwork.artistID 
        JOIN on_exhibition ON artwork.artworkID = on_exhibition.artworkID 
        JOIN exhibition ON on_exhibition.exhibitionID = exhibition.exhibitionID 
        JOIN location ON exhibition.locationID = location.locationID 
        WHERE artist.birthplace = location.city 
        ORDER BY artist.name ASC, exhibition.title ASC; 
    """
    args = ["exNumber = 0", "show_answer_difference", "feedback=join"]

    answer, output = run_test_case(ans_query, ref_query, args)
    returned_msgs = parse_flag_msg(output, 0)
    error_keys = ["IncorrectResult"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    returned_msgs = parse_flag_msg(output, 2)
    error_keys = ["incorrectJoin", "AdditionalTests"]
    correct_msgs = get_msg("en", error_keys)
    assert compare_messages(returned_msgs, correct_msgs)

    assert not answer