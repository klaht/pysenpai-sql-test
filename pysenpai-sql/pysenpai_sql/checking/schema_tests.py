import sqlite3

def check_table_names():
    pass

def check_column_names():
    pass

def check_column_data_types():
    pass

def check_primary_key(answer_columns, ref_columns):
    assert answer_columns #Assert list isn't empty

    for i, correct_column in enumerate(ref_columns):
        if correct_column[5] != answer_columns[i][5]:
            return "incorrect_primary_key"

    return None

def check_null_values_allowed():
    pass