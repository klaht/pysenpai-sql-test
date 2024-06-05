from pysenpai import core
from SELECT_test_main import execute_test as selectTestExecute 
from INSERT_test_main import execute_test as insertTestExecute 

# TODO 
#   Set messages like is done in seperate main files
#   Clean previous main files
#   Add support for database seeding files 
#   Insert queries and test queries? 

if __name__ == "__main__":

    args, language = core.parse_command()
    try: 
        answerFile = args[0]; referenceFile = args[1]

        reference_query = open(referenceFile).readline()
        assignmentType = reference_query.split()[0]

        match assignmentType.upper():
            case "SELECT":
                selectTestExecute(reference_query)
            case "INSERT":
                insertTestExecute(reference_query)
                

                

    except IndexError:
        print("USAGE: ANSWER_FILENAME REFERENCE_FILENAME")