import sqlite3

schema_indices = [
    "incorrect_query",
    "incorrect_column_name",
    "incorrect_data_type",
    "incorrect_not_null",
    "incorrect_default_value",
    "incorrect_primary_key",
]

def assertOrder(res, correct):
    '''Checks if the list is sorted in ascending order'''

    if res != correct and set(res) == set(correct):
        return "incorrect_return_order", None

    return None, None

def assertSelectedVariables(res, correct):
    '''Checks if the list contains the correct variables and that they are in the correct order'''

    if res == correct:
        return None, None

    for i, value in enumerate(correct):
        if len(res[i]) != len(value):
            return "incorrect_selected_columns", None
        
        #Only need to compare the first indices
        break

    return None, None

def evaluate_variables(res, correct):
    '''Checks if the list contains the correct variables and that they are in the correct order'''
    correct = [list(row) for row in correct][0] # Arrange result to list
    res = [list(row) for row in res][0] # Arrange result to list

    for i, item in enumerate(res): # Check if missing or incorrect values

        if item == None: # Missing value
            return "MissingInsertedValueError", None
        elif item != correct[i]: # Correct value
            return "IncorrectInsertError", item

    
    return None

def assertDistinct(res, correct):
    '''Checks if the list contains only distinct values'''
    #TODO Implement correctly
    
    for thing in res:
        if res.count(thing) > 1:
            return "output_not_distinct", None
        return None, None

def evaluateAmount(res, correct):
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

def checkTableName(correct_table_names = ['']):
    '''Checks if the table name is correct'''
    
    #TODO:
    #FIX THIS, NO HARD CODING

    default_table_names = [('Artist',), ('Location',), ('Collection',), ('ArtWork',), ('Exhibition',), ('On_Exhibition',)]

    conn = sqlite3.connect("mydatabase1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()

    correct_table_names = set(correct_table_names)
    table_name = set(table_name)
    default_table_names = set(default_table_names)

    table_name = table_name - default_table_names
    if table_name != correct_table_names:
        return ("incorrect_table_name")
    return None

def checkTableColumns(req_column_names = ['']):
    '''Checks if the table columns are correct'''

    conn = sqlite3.connect("mydatabase1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM testtable")
    column_names = [column[0] for column in cursor.description]
    if column_names != req_column_names:
        return ("incorrect_column_name")
    return None

def evaluate_updated_values(res, correct):
    '''Checks if the updated values contains correct values'''
    try:
        for i, value in enumerate(res):
            if value != correct[i]:
                return ("IncorrectUpdatedValues"), res
    except IndexError:
        return "incorrect_selected_rows", res

    return None, None

def compare_column_data(res, correct):
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

def check_table_schema(res, correct):
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

def check_table_content_after_delete(res, correct):
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
    "update": evaluate_updated_values
}
