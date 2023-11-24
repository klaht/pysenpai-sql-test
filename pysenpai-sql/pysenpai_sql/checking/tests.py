import sqlite3

def assertOrder(res, order):
    '''Checks if the list is sorted in ascending order'''

    if order == "ASC":
        sorted_res = sorted(res)
    elif order == "DESC":
        sorted_res = sorted(res, reverse=True)
    else:
        sorted_res = "ASC" # ASC by default

    if res != sorted_res:
        return ("incorrect_return_order")
    return None


def assertSelectedVariables(res, correct):
    '''Checks if the list contains the correct variables and that they are in the correct order'''

    res = [item.lower() for item in res]
    correct = [item.lower() for item in correct]

    incorrect_variables = res != correct
    incorrect_order = sorted(res) == (sorted(correct)
                                                and incorrect_variables)
    if incorrect_order:
        return ("incorrect_column_order")
    elif incorrect_variables:
        return ("incorrect_selected_columns")
    return None

def evaluate_variables(res, correct):
    '''Checks if the list contains the correct variables and that they are in the correct order'''
    correct = [list(row) for row in correct][0] # Arrange result to list

    for i, item in enumerate(res): # Check if missing or incorrect values

        if item == None: # Missing value
            return ("MissingInsertedValueError")
        elif item != correct[i]: # Correct value
            return ("IncorrectInsertError")

    
    return None
    

def assertDistinct(res):
    '''Checks if the list contains only distinct values'''
    
    for thing in res:
        if res.count(thing) > 1:
            return ("output_not_distinct")
        return None

def assertDistinct(res):
    '''Checks if the list contains only distinct values'''
    
    for thing in res:
        if res.count(thing) > 1:
            return ("output_not_distinct")
        return None

def evaluateAmount(res, correct, exNumber):
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
            message = "too_many_return_values" + str(exNumber)
            return (message), excessive
    
    elif len(set_evaluated) < len(set_correct):
        excessive = set_correct - set_evaluated
        if set_evaluated != set_correct:
            message = "too_little_return_values" +  str(exNumber)
            return (message), excessive

    return None, None

def checkTableName():
    '''Checks if the table name is correct'''

    conn = sqlite3.connect("mydatabase1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()
    if table_name.__contains__("testtable") == False:
        return ("incorrect_table_name")
    return None