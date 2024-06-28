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
        return "incorrect_table_name", None
    
    return None, None
    

def checkTableNameFromDB(res, correct, feedback_params=None):
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

def checkTableColumns(res, correct, feedback_params=None):
    '''Checks if the table columns are correct'''

    correct_answer = feedback_params['ref']
    student_answer_file = feedback_params['res']
    
    try :
        student_answer1 = open(student_answer_file, 'r')
        student_answer = student_answer1.read()
    except FileNotFoundError as e:
        return None, None
    
    correct_column_names = get_column_names_from_query(correct_answer)
    res_column_names = get_column_names_from_query(student_answer)
    
    if correct_column_names.lower() != res_column_names.lower():
        return "incorrect_column_name", None
        
    return None, None

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

def evaluate_multi_query_content(res, correct, feedback_params=None):
    res_tables: dict = feedback_params['ans_multi_result']
    ref_tables: dict = feedback_params['ref_multi_result']

    for table, value in ref_tables.items():
        for i, row in enumerate(value['content']):
            if row != res_tables[table]['content'][i]:
                return "multi_incorrect_table_content", table

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
    "multi_content": evaluate_multi_query_content,
    "multi_schema": evaluate_multi_query_schema,
    "table_name": check_table_names_from_query,
    "column_names": checkTableColumns
}

#Helper functions
            
def get_table_names_from_query(query):
   
    table_ids = None
    table_names = ""
    ignore_once = False
    
    if "FROM" in query:
        table_ids = query.index("FROM") + 5
    if "INTO" in query:
        table_ids = query.index("INTO") + 5
    if "TABLE" in query:
        table_ids = query.index("TABLE") + 6
   
    if table_ids != None:
        while table_ids < len(query) and (query[table_ids] != " " and query[table_ids] != ";") or ignore_once == True:
            table_names += query[table_ids]
            table_ids += 1
            ignore_once = False
            if table_names[len(table_names)-1] == ",": #if multpiple tables they are separated by a comma
                ignore_once = True
    
    return table_names

def get_column_names_from_query(query):
    
    column_ids = None
    column_names = ""
    ignore_once = False
    
    if "SELECT" in query:
        column_ids = query.index("SELECT") + 7
    if "UPDATE" in query:
        column_ids = query.index("UPDATE") + 7
    if "DISTINCT" in query:
        column_ids = query.index("DISTINCT") + 9
    if "SET" in query:
        column_ids = query.index("SET") + 4
    
    if column_ids != None:
        while column_ids < len(query) and (query[column_ids] != " " and query[column_ids] != ";") or ignore_once == True:
            column_names += query[column_ids]
            column_ids += 1
            ignore_once = False
            if column_names[len(column_names)-1] == ",":
                ignore_once = True
                
    return column_names
    