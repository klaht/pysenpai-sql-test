import pysenpai.core as core

def create_feedback_messages(msgs):
    """
    Creates feedback messages for the tests.
    """

    msgs.set_msg("fail_output_result", "fi", dict(
        content="Pääohjelman tulostama tulos oli väärä.",
        triggers=["student_sql_query"]
    ))
    msgs.set_msg("fail_output_result", "en", dict(
        content="The result printed by the main program was wrong.",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("incorrect_return_order", "fi", dict(
        content="Palautettava listaa ei järjestetty oikein.",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("incorrect_return_order", "en", dict(
        content="The list was not arranged correctly.",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("incorrect_selected_columns", "fi", dict(
        content="Haussa käyttettiin vääriä sarakkeita.",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("incorrect_selected_columns", "en", dict(
        content="The query used wrong columns.",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("incorrect_column_order", "fi", dict(
        content="Virheellinen sarakkeiden järjestys",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("incorrect_column_order", "en", dict(
        content="Invalid column order.",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("too_many_return_values", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja {output}",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("too_many_return_values", "en", dict(
        content="The result contained too many values {output}",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("too_little_return_values", "fi", dict(
        content="Tulos sisälsi liian vähän palautusarvoja {output}",
        triggers=["student_sql_query"]
    ))

    msgs.set_msg("too_little_return_values", "en", dict(
        content="The result contained too low amount of values {output}", 
        triggers=["student_sql_query"]
    ))

    # For Exercise 1
    msgs.set_msg("too_many_return_values1", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, " 
        "Varmista, että valitset vain SUOMALAISTEN taiteilijoiden tietoja"
        "Ylimääräiset arvot: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 1
    msgs.set_msg("too_many_return_values1", "en", dict(
        content="The result contained too many return values, " 
        "Make sure, that you are only selecting information about FINNISH artists."
        "Excessive values: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 2
    msgs.set_msg("too_many_return_values2", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, "
        "Varmista, että valitset vain TAULUJA, joiden HINTA on YLI 1000000."
        "Ylimääräiset arvot: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 2
    msgs.set_msg("too_many_return_values2", "en", dict(
        content="The result contained too many return values, "
        "Make sure, that you are only selecting PAINTINGS, that have a PRICE over 1000000."
        "Excessive values: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 3
    msgs.set_msg("too_many_return_values3", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, "
        "Varmista, että valitset vain MUSEOITA, OULUSTA ja HELSINGISTÄ."
        "Ylimääräiset arvot: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 3
    msgs.set_msg("too_many_return_values3", "en", dict(
        content="The result contained too many return values, "
        "Make sure, that you are only selecting MUSEUMS from OULU and HELSINKI."
        "Excessive values: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 3
    msgs.set_msg("too_little_return_values3", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, "
        "Varmista, että valitset MUSEOITA MOLEMMISTA, OULUSTA ja HELSINGISTÄ."
        "Puuttuvat arvot: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 3
    msgs.set_msg("too_little_return_values3", "en", dict(
        content="The result contained too little return values, "
        "Make sure, that you are selecting MUSEUMS from BOTH OULU and HELSINKI."
        "Missing values: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 4
    msgs.set_msg("too_many_return_values4", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, "
        "Varmista, että valitset vain teokset, joiden TYYPPI on MAALAUS TAI VEISTOS, sekä hinta on SUUREMPI kuin 50000."
        "Ylimääräiset arvot: {output}",
        triggers=["student_sql_query"]
    ))
    
    # For Exercise 4
    msgs.set_msg("too_many_return_values4", "en", dict(
        content="The result contained too many return values, "
        "Make sure, that you are only selecting artwork, which type is PAINTING OR SCUPLTURE, and the price is GREATER than 50000."
        "Excessive values: {output}",
        triggers=["student_sql_query"]
    ))
        
    # For Exercise 4
    msgs.set_msg("too_little_return_values4", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, "
        "Varmista, että valitset teokset, joiden TYYPPI on MAALAUS TAI VEISTOS, sekä hinta on SUUREMPI kuin 50000."
        "Puuttuvat arvot: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 4
    msgs.set_msg("too_little_return_values4", "en", dict(
        content="The result contained too little return values, "
        "Make sure, that you are selecting artwork, which type is PAINTING OR SCUPLTURE, and the price is GREATER than 50000."
        "Missing values: {output}",
        triggers=["student_sql_query"]
    ))

    # For Exercise 5
    msgs.set_msg("too_many_return_values5", "fi", dict(
        content="Tulos sisälsi liikaa palautusarvoja, "
        "Varmista, että valitset vain näyttelyt, joissa kävijämäärä ON olemassa."
        "Ylimääräiset arvot: {output}",
        triggers=["student_sql_query"]
    ))
    
    # For Exercise 5
    msgs.set_msg("too_many_return_values5", "en", dict(
        content="The result contained too many return values, "
        "Make sure, that you are only exhibitions, which have a VISITOR AMOUNT."
        "Excessive values: {output}",
        triggers=["student_sql_query"]
    ))