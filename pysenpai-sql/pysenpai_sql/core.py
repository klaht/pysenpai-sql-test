import io
import os.path
import sys
import sqlite3
import pysenpai.callbacks.defaults as defaults
from pysenpai.output import json_output
from pysenpai.messages import load_messages, Codes
from pysenpai.output import output
from pysenpai.utils.internal import FNAME_PAT


def load_sql_module(
                module_path,
                lang="en",
                custom_msgs={},
                inputs=[],
                hide_output=True,
                allow_output=True,
                presenter=defaults.default_input_presenter):

    """
    Checks if the student answer is in correct format.
    Setups the databases for testing.
    Setups the output.

    * *lang* - language for messages
    * *custom_msgs* - a TranslationDict object that
      includes additions/overrides
      to the default import messages
    * *inputs* - input vector to be given to the program;
      inputs are automatically joined
      by newlines and made into a StringIO object that replaces standard input.
      When calling this function you need to provide inputs that allow
      the program to execute
      without errors.
    * *hide_output* - a flag to hide or show output,
       by default output is hidden
    * *allow_output* - a flag that dictates whether it's considered an error
       if the code has output or not. By default output is allowed.
    * *presenter* - a presenter function for showing inputs
       in the output in case of errors
       
    returns False if an error occurs, otherwise returns True
    """

    # save = sys.stdout
    msgs = load_messages(lang, "import")
    msgs.update(custom_msgs)
    module_name = os.path.basename(module_path)

    json_output.new_test(msgs.get_msg("LoadingModule", lang)
                         ["content"].format(name=module_name))
    json_output.new_run()

    #dberror = create_databases(msgs, lang)
    #if (dberror == False):
    #    return False
    if not module_name.endswith(".sql"):
        output(msgs.get_msg("MissingFileExtension", lang), Codes.ERROR)
        print("MissingFileExtension")
        return False

    name = module_name.rsplit(".sql", 1)[0]

    if not FNAME_PAT.fullmatch(name):
        output(msgs.get_msg("BadModuleName", lang),
               Codes.ERROR, name=module_name)
        print("BadModuleName")
        return False

    # pyver = "{}.{}".format(sys.version_info.major, sys.version_info.minor)

    if name in sys.stdlib_module_names:
        output(msgs.get_msg("SystemModuleName", lang),
               Codes.ERROR, name=module_name)
        print("SystemModuleName")
        return False

    if inputs:
        sys.stdin = io.StringIO("\n".join([str(i) for i in inputs]))
        
    return True

def create_databases(msgs, lang):
    
    """
    Creates two similar databases for testing.
    
    * *msgs* - messages for output
    * *lang* - language for messages
    
    returns False if an error occurs, True otherwise
    
    """
    
    try:
        sql_file = open("data.sql", 'r')
        sql_script = sql_file.read()

    except FileExistsError as e:
        output(msgs.get_msg("FileNotFoundError", lang),
               Codes.ERROR)
        return False
    
    try:
        conn = sqlite3.connect("mydatabase1.db")
        cursor = conn.cursor()

        cursor.executescript(sql_script)

        conn.commit()
        conn.close()

        conn2 = sqlite3.connect("mydatabase2.db")
        cursor2 = conn2.cursor()

        cursor2.executescript(sql_script)

        conn2.commit()
        conn2.close()

    except sqlite3.Error as e:
        output(msgs.get_msg("DatabaseCreationError", lang),
               Codes.ERROR)
        return False
    
    return True
