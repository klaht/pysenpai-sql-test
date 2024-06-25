import sqlite3

schema_indices = [
    "incorrect_query",
    "incorrect_column_name",
    "incorrect_data_type",
    "incorrect_not_null",
    "incorrect_default_value",
    "incorrect_primary_key",
]

def assertOrder(res, correct, feedback_params=None):
    '''Checks if the list is sorted in ascending order'''

    if res != correct and set(res) == set(correct):
        return "incorrect_return_order", None

    return None, None

def assertSelectedVariables(res, correct, feedback_params=None):
    '''Checks if the list contains the correct variables and that they are in the correct order'''

    if res == correct:
        return None, None

    for i, value in enumerate(correct):
        if len(res[i]) != len(value):
            return "incorrect_selected_columns", None
        
        #Only need to compare the first indices
        break

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

def assertDistinct(res, correct, feedback_params=None):
    '''Checks if the list contains only distinct values'''
    #TODO Implement correctly
    
    for thing in res:
        if res.count(thing) > 1:
            return "output_not_distinct", None
        return None, None

def evaluateAmount(res, correct, feedback_params=None):
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

def check_table_names_from_query(res, correct):
    '''
    Checks if the table names are correct in the query
    Can be used for everything
    ''' 
    
    correct_table_ids = None
    res_table_ids = None
    correct_table_names = None
    res_table_names = None
    
    if "FROM" in correct:
        correct_table_ids = correct.index("FROM")
    if "INTO" in correct:
        correct_table_ids = correct.index("INTO")
    if "TABLE" in correct:
        correct_table_ids = correct.index("TABLE")    
    
    if correct_table_ids != None:
        correct_table_names = correct[correct_table_ids + 1]
    
    if "FROM" in res:
        res_table_ids = res.index("FROM")
    if "INTO" in res:
        res_table_ids = res.index("INTO")
    if "TABLE" in res:
        res_table_ids = res.index("TABLE")
    
    if res_table_ids != None:    
        res_table_names = res[res_table_ids + 1]
    
    if correct_table_names != res_table_names:
        return "incorrect_table_name", None
    
    return None, None
    

def checkTableNameFromDB(correct_table_names = ['']):
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
        return ("incorrect_table_name")
    return None

def checkTableColumns(req_column_names = [''], feedback_params=None):
    '''Checks if the table columns are correct'''

    conn = sqlite3.connect("mydatabase1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM testtable")
    column_names = [column[0] for column in cursor.description]
    if column_names != req_column_names:
        return ("incorrect_column_name")
    return None

def evaluate_updated_values(res, correct, feedback_params=None):
    incorrect_where_clause = feedback_params['res_affected_ids'] != feedback_params['correct_affected_ids']
    '''Check if correct rows have been affected'''
    if len(res) != len(correct) or incorrect_where_clause:
        return "incorrect_selected_rows", res

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
                return "incorrect_selected_columns"
    except IndexError:
        return "incorrect_selected_columns"
    
    return None

def check_table_schema(res, correct, feedback_params=None):
    res_table_name = res.pop()
    correct_table_name = correct.pop()

    if correct_table_name != res_table_name:
        return "incorrect_table_name", None
    
    if len(res) != len(correct):
        return "incorrect_column_amount", None

    for i, value in enumerate(correct):
        for j in range (0, 6):
            if res[i][j] != value[j]:
                return schema_indices[j], None

def check_table_content_after_delete(res, correct, feedback_params=None):
    if len(correct) > len(res):
        return "too_few_deleted", None
    elif len(correct) < len(res):
        return "too_many_deleted", None
    
    for i, value in enumerate(res):
        if value != correct[i]:
            return "incorrect_deleted_rows", None




feedback_functions = {
    "value": evaluate_variables,
    "schema": check_table_schema,
    "delete": check_table_content_after_delete,
    "order": assertOrder,
    "distinct": assertDistinct,
    "selected_columns": assertSelectedVariables,
    "amount": evaluateAmount,
    "column": compare_column_data,
    "update": evaluate_updated_values,
    "table_name": check_table_names_from_query
}

#Helper functions
def get_affected_row_ids(cursor: sqlite3.Cursor, query):
    """
    Get all affected row primary keys from an update query
    Splits the query at the first WHERE and uses the part after in a SELECT query
    """
    where_clause = re.split("where", query, maxsplit=1, flags=re.IGNORECASE)[1]
    primary_key = getTablePrimaryKey(cursor, query)

    affected_query = "SELECT " + primary_key + " FROM " + query.split()[1] + " WHERE " + where_clause

    cursor.execute(affected_query)

    return cursor.fetchall()

def get_rows_with_ids(cursor, query, ids):
    """
    Get all rows from table for given ids (primary key)
    """
    primary_key = getTablePrimaryKey(cursor, query)
    select_query = "SELECT * FROM " + query.split()[1] + " WHERE " + primary_key + " IN " +  ids_to_string(ids) 
    cursor.execute(select_query)

    return cursor.fetchall()

def getTablePrimaryKey(cursor, query):
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
