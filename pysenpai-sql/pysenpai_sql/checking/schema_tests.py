import sqlite3
"""
Test column data retrieved with PRAGMA table_info({tablename});
Documentation: https://sqlite.org/pragma.html#pragma_table_info:~:text=PRAGMA%20schema.table_info(table%2Dname)%3B
Description of list indices (from sqlite) [?, name, type, notnull, default_value, primary_key]
"""
COLUMN_NAME = 1
DATA_TYPE = 2
NOT_NULL = 3  
DEFAULT_VALUE = 4
PRIMARY_KEY = 5

def check_table_names(ans_table_name, ref_table_name):
    if ans_table_name != ref_table_name:
        return "incorrect_table_name"

def check_column_names(answer_columns, ref_columns):
    assert answer_columns #Assert list isn't empty

    for i, correct_column in enumerate(ref_columns):
        if correct_column[COLUMN_NAME] != answer_columns[i][COLUMN_NAME]:
            return "incorrect_column_name"

    return None

def check_column_data_types(answer_columns, ref_columns):
    assert answer_columns #Assert list isn't empty

    for i, correct_column in enumerate(ref_columns):
        if correct_column[DATA_TYPE] != answer_columns[i][DATA_TYPE]:
            return "incorrect_data_type"

    return None

def check_primary_key(answer_columns, ref_columns):
    assert answer_columns #Assert list isn't empty

    for i, correct_column in enumerate(ref_columns):
        if correct_column[PRIMARY_KEY] != answer_columns[i][PRIMARY_KEY]:
            return "incorrect_primary_key"

    return None

def check_null_values_allowed(answer_columns, ref_columns):
    assert answer_columns #Assert list isn't empty

    for i, correct_column in enumerate(ref_columns):
        if correct_column[NOT_NULL] != answer_columns[i][NOT_NULL]:
            return "incorrect_not_null"

    return None