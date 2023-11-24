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

def evaluate_variables(res):
    '''Checks if the list contains the correct variables and that they are in the correct order'''
    for item in res: # Check if missing values if item == None: output(msgs.get_msg("IncorrectResult", lang), Codes.ERROR) return 0, 0
        if item == None: 
            return ("incorrect_selected_columns")
    
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

def checkPrimaryKey(student_answer, insert_query):
    '''Checks if the student answer contains a primary key'''
    
    try :
        sql_file = open(student_answer, 'r')
        sql_script = sql_file.read()
    except FileNotFoundError as e:
        return "file_open_error"
        
    # Run student answer
    try: 
        conn = sqlite3.connect("mydatabase1.db")
        cursor = conn.cursor()
        primary_key_test = "INSERT INTO testtable VALUES (1, 'testi2')"

        cursor.executescript(sql_script)
        # Insert to created table
        cursor.executescript(insert_query)

        cursor.execute(primary_key_test)            

        conn.commit()
        cursor.close()
        conn.close()
        
    except sqlite3.IntegrityError as e:
        return None
    
    yield "no_primary_key"