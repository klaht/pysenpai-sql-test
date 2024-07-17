import sqlite3
import re

schema_indices = [
    "incorrect_query",
    "incorrect_column_name",
    "incorrect_data_type",
    "incorrect_not_null",
    "incorrect_default_value",
    "incorrect_primary_key",
]

def assert_order(res, correct, feedback_params=None):
    '''Checks if the list is sorted in ascending order'''

    student_answer = feedback_params['res']
    #Check if query contains order keyword
    if not re.search(r"\bORDER\s+BY\b", student_answer, re.IGNORECASE):
        return "noOrderByKeyword", None

    if res != correct and set(res) == set(correct):
        return "incorrectReturnOrder", None

    return None, None

def assert_selected_variables(res, correct, feedback_params=None):
    '''Checks if the list contains the correct variables and that they are in the correct order'''

    correct_answer = feedback_params['ref']
    student_answer = feedback_params['res']

    if res == correct:
        return None, None

    if len(res) == 0:
        return "noSelectedRows", None

    student_columns = get_column_names_from_query(student_answer).split(",")
    reference_columns = get_column_names_from_query(correct_answer).split(",")

    if len(student_columns) != len(reference_columns):
        return "incorrectSelectedColumnAmount", None

    for i, column in enumerate(reference_columns):
        if column.strip() != student_columns[i].strip():
            return "unmatchedColumn", student_columns[i]

        

    return None, None

def evaluate_variables(res, correct, feedback_params=None):
    '''Checks if the list contains the correct variables and that they are in the correct order'''
    correct = [list(row) for row in correct][0] # Arrange result to list
    res = [list(row) for row in res][0] # Arrange result to list

    for i, item in enumerate(res): # Check if missing or incorrect values

        if item == None: # Missing value
            return "MissingInsertedValueError", None
        elif item != correct[i]: # Correct value
            return "IncorrectInsertError", item

    
    return None

def assert_distinct(res, correct, feedback_params=None):
    '''Checks if the list contains only distinct values and if the query contains distinct keyword'''
    student_answer = feedback_params['res']
    if not re.search(r"\bDISTINCT\b", student_answer, re.IGNORECASE):
        return "noDistinctKeyword", None
    
    for thing in res:
        if res.count(thing) > 1:
            return "outputNotDistinct", None
        return None, None

def evaluate_amount(res, correct, feedback_params=None):
    '''
    Checks if the answer contains the correct amount of values
    If there are too many or too little values, returns the excessive values
    '''

    evaluated_answer_tuples = [(artist,) for artist in res]

    set_evaluated = set(evaluated_answer_tuples)
    set_correct = set(correct)

    if len(set_evaluated) > len(set_correct):
        excessive = set_evaluated - set_correct
        if set_evaluated != set_correct:
            message = "too_many_return_values"
            return (message), excessive
    
    elif len(set_evaluated) < len(set_correct):
        excessive = set_correct - set_evaluated
        if set_evaluated != set_correct:
            message = "too_little_return_values"
            return (message), excessive

    return None, None

def check_table_names_from_query(res, correct, feedback_params=None):
    '''
    Checks if the table names are correct in the query
    Can be used for everything
    ''' 
    
    correct_answer = feedback_params['ref']
    student_answer_file = feedback_params['res']
    
    try :
        student_answer1 = open(student_answer_file, 'r')
        student_answer = student_answer1.read()
    except FileNotFoundError as e:
        return None, None
        
    correct_table_names = get_table_names_from_query(correct_answer)
    res_table_names = get_table_names_from_query(student_answer)
    
    if correct_table_names.lower() != res_table_names.lower():
        return "incorrectTableName", None
    
    return None, None
    

def check_table_name_from_db(res, correct, feedback_params=None):
    '''
    Checks if the table names are correct in the modified database
    Used for UPDATE AND DELETE!!!!
    '''

    # Gets the table names from the student's database
    conn = sqlite3.connect("mydatabase1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()

    # Gets the table names from the reference database
    conn2 = sqlite3.connect("mydatabase2.db")
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    correct_table_names = cursor2.fetchall()

    # Compares the table names
    if table_name != correct_table_names:
        return ("incorrectTableName")
    return None

def check_table_columns(res, correct, feedback_params=None):
    '''Checks if the table columns are correct'''

    correct_answer = feedback_params['ref']
    student_answer = feedback_params['res']
    
    correct_column_names = get_column_names_from_query(correct_answer)
    res_column_names = get_column_names_from_query(student_answer)
    
    if correct_column_names.lower() != res_column_names.lower():
        return "incorrectColumnName", None
        
    return None, None

def evaluate_updated_values(res, correct, feedback_params=None):
    incorrect_where_clause = feedback_params['res_affected_ids'] != feedback_params['correct_affected_ids']
    '''Check if correct rows have been affected'''
    if len(res) != len(correct) or incorrect_where_clause:
        return "incorrectSelectedRows", res

    '''Checks if the updated values contains correct values'''
    for i, value in enumerate(res):
        if value != correct[i]:
            return ("IncorrectUpdatedValues"), res

    return None, None

def compare_column_data(res, correct, feedback_params=None):
    '''
    Compare column values of reference and answer table
    '''
    try:
        for i, column in enumerate(correct):
            if column != res[i]:
                return "incorrectSelectedColumns"
    except IndexError:
        return "incorrectSelectedColumns"
    
    return None

def check_table_schema(res, correct, feedback_params=None):
    res_table_name = res.pop()
    correct_table_name = correct.pop()

    if correct_table_name != res_table_name:
        return "incorrectTableName", None
    
    if len(res) != len(correct):
        return "incorrectColumnAmount", None

    for i, value in enumerate(correct):
        for j in range (0, 6):
            if res[i][j] != value[j]:
                return schema_indices[j], None

def check_table_content_after_delete(res, correct, feedback_params=None):
    if len(correct) > len(res):
        return "tooFewDeleted", None
    elif len(correct) < len(res):
        return "tooManyDeleted", None
    
    for i, value in enumerate(res):
        if value != correct[i]:
            return "incorrectDeletedRows", None

def evaluate_multi_query_content(res, correct, feedback_params=None):
    res_tables: dict = feedback_params['ans_multi_result']
    ref_tables: dict = feedback_params['ref_multi_result']

    for table, value in ref_tables.items():
        for i, row in enumerate(value['content']):
            if row != res_tables[table]['content'][i]:
                return "multiIncorrectTableContent", table

    return None, None

def evaluate_multi_query_schema(res, correct, feedback_params=None):
    res_tables: dict = feedback_params['ans_multi_result']
    ref_tables: dict = feedback_params['ref_multi_result']

    for table, value in ref_tables.items():
        for i, value in enumerate(value['data']):
            for j in range (0, 6):
                if res_tables[table]['data'][i][j] != value[j]:
                    return schema_indices[j], table

    return None, None

def check_group_by(res, correct, feedback_params=None):
    '''
    Test if query contains GROUP BY keyword
    and correct parameters are used
    '''
    student_answer = feedback_params['res']
    reference_answer = feedback_params['ref']

    student_group_by = get_group_by_parameter_from_query(student_answer)
    if not student_group_by:
        return "noGroupByKeyword", None

    reference_group_by = get_group_by_parameter_from_query(reference_answer)

    if reference_group_by and (student_group_by != reference_group_by):
        return "incorrectGroupBy", None

    answer_having_param = get_group_by_having_paramater(student_answer)
    reference_having_param = get_group_by_having_paramater(reference_answer)

    if reference_having_param and not answer_having_param:
        return "noHavingKeyword", None

    if reference_having_param and answer_having_param != reference_having_param:
        return "incorrectHavingKeyword", None
    
    return None, None

def evaluate_joins(res:list, correct:list, feedback_params=None):
    student_answer = feedback_params['res']
    reference_answer = feedback_params['ref']

    student_joins = get_joins(student_answer)
    reference_joins = get_joins(reference_answer)

    for table, joins in reference_joins.items():
        student_join_for_table = student_joins.get(table, None)

        if not student_join_for_table:
            return "tableNotJoined", table
        
        if student_join_for_table != joins:
            return "incorrectJoin", None

    if len(student_joins) != len(reference_joins):
        return "incorrectJoin", None

    return None, None

feedback_functions = {
    "value": evaluate_variables,
    "schema": check_table_schema,
    "delete": check_table_content_after_delete,
    "order": assert_order,
    "distinct": assert_distinct,
    "selected_columns": assert_selected_variables,
    "amount": evaluate_amount,
    "column": compare_column_data,
    "update": evaluate_updated_values,
    "multi_content": evaluate_multi_query_content,
    "multi_schema": evaluate_multi_query_schema,
    "table_name": check_table_names_from_query,
    "column_names": check_table_columns,
    "group_by": check_group_by,
    "join": evaluate_joins
}

#Helper functions

def get_joins(query:str) -> dict:
    joins = {}
    aliases = get_aliases(query)
    raw_joins = re.findall("JOIN\s+(\w+)(?:\s+AS\s+\w+)?\s+ON\s+([\.\w]+)\s*=\s*([\.\w]+)", query, re.IGNORECASE)

    for table_name, left, right in raw_joins:
        joins[aliases.get(table_name, table_name)] = (
            replace_alias(left, aliases), 
            replace_alias(right, aliases)
        )
    
    return joins
        
        

def replace_alias(join_param:str, aliases:dict):
    table, column = join_param.split(".")
    
    return aliases.get(table, table) + "." + column


def get_aliases(query:str) -> dict:
    alias_and_value = {}
    aliases = re.findall(r"(\w+)\s+AS\s+(\w+)", query, flags=re.IGNORECASE)
    for alias in aliases:
       alias_and_value[alias[1]] = alias[0]
    
    return alias_and_value


def get_group_by_parameter_from_query(query):
    group_by_param = re.search(r"\bGROUP\s+BY\s+(\w+)\b", query, re.IGNORECASE)
    if group_by_param:
        return group_by_param.group(1)
    
    return False

def get_group_by_having_paramater(query):
    having_param = re.search(r"\bGROUP\s+BY\s+[\w\.]+\s+HAVING\s+(.+)(?:;|\bORDER\s+BY\b)", query, re.IGNORECASE)
    if having_param:
        return having_param.group(1)
    
    return False
            
def get_affected_row_ids(cursor: sqlite3.Cursor, query):
    """
    Get all affected row primary keys from an update query
    Splits the query at the first WHERE and uses the part after in a SELECT query
    """
    where_clause = re.split("where", query, maxsplit=1, flags=re.IGNORECASE)[1]
    primary_key = get_table_primary_key(cursor, query)

    affected_query = "SELECT " + primary_key + " FROM " + query.split()[1] + " WHERE " + where_clause

    cursor.execute(affected_query)

    return cursor.fetchall()

def get_rows_with_ids(cursor, query, ids):
    """
    Get all rows from table for given ids (primary key)
    """
    primary_key = get_table_primary_key(cursor, query)
    select_query = "SELECT * FROM " + query.split()[1] + " WHERE " + primary_key + " IN " +  ids_to_string(ids) 
    cursor.execute(select_query)

    return cursor.fetchall()

def get_table_primary_key(cursor, query):
    """
    Get primary key from an UPDATE query
    Uses PRAGMA query to fetch information about the table
    """
    table_name = query.split()[1]
    columns_query = "PRAGMA table_info(" + table_name + ")"
    columns = cursor.execute(columns_query).fetchall()

    for column in columns:
        if column[5]: #Primary key information is stored at index 5
            try:
                return column[1] #Index 1 stores column name
            except Exception as e:
                raise IndexError

def get_table_names_from_query(query):
    result = re.search(r"\b(?:FROM|INTO|TABLE)\s+(\w+(?:,\s*\w+)*).*;", query, re.IGNORECASE)

    return result.group(1).replace(" ", "")


def get_column_names_from_query(query):
    '''TODO Support for other query types'''
    result = re.search(r"\b(?:SELECT(?: DISTINCT)?)(.*)\bFROM\b", query, re.IGNORECASE)

    return result.group(1).replace(" ", "")
