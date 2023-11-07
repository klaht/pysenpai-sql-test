import io
import os.path
import sys
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
    load_module(module_path[, lang="en"][, custom_msgs={}][, inputs=[]][, hide_output=True][, allow_output=True][, presenter=default_input_presenter]) -> Module
    
    This function imports the student module and needs to be called before doing tests.
    The parameters are
    
    * *lang* - language for messages
    * *custom_msgs* - a TranslationDict object that includes additions/overrides 
      to the default import messages
    * *inputs* - input vector to be given to the program; inputs are automatically joined 
      by newlines and made into a StringIO object that replaces standard input. When 
      calling this function you need to provide inputs that allow the program to execute
      without errors. 
    * *hide_output* - a flag to hide or show output, by default output is hidden
    * *allow_output* - a flag that dictates whether it's considered an error if the code
      has output or not. By default output is allowed.
    * *presenter* - a presenter function for showing inputs in the output in case of
      errors
       
    Before attempting to import the student module, the function checks whether the 
    filename is a proper Python module name. None is returned if the filename is
    invalid. This also happens if the module has the same name as a Python library module.
    
    If importing the student module results in an exception, the exception's name is
    looked up from the message dictionary and the corresponding error message is
    shown in the checker output. If the exception name is not found, GenericErrorMsg
    is shown instead. See :ref:`Output Messages <output-messages>` for information
    about how to specify your own error messages. 
    
    If importing is successful and *allow_output* is set to False, the StringOutput
    object is checked for prints and an error message is given if content is found.
    Otherwise the module object is returned.    
    """

    save = sys.stdout
    msgs = load_messages(lang, "import")
    msgs.update(custom_msgs)
    module_name = os.path.basename(module_path)
    
    json_output.new_test(msgs.get_msg("LoadingModule", lang)["content"].format(name=module_name))
    json_output.new_run()
    
    if not module_name.endswith(".sql"):
        output(msgs.get_msg("MissingFileExtension", lang), Codes.ERROR)
        print("MissingFileExtension")
        return None
    
    name = module_name.rsplit(".sql", 1)[0]
    
    if not FNAME_PAT.fullmatch(name):    
        output(msgs.get_msg("BadModuleName", lang), Codes.ERROR, name=module_name)
        print("BadModuleName")
        return None
        
    pyver = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
        
    if name in sys.stdlib_module_names:
        output(msgs.get_msg("SystemModuleName", lang), Codes.ERROR, name=module_name)
        print("SystemModuleName")
        return None
   
    if inputs:
        sys.stdin = io.StringIO("\n".join([str(i) for i in inputs]))
    """  
    o = StringOutput()
    sys.stdout = o
   
    try:        
        st_module = importlib.import_module(name)
    except:
        sys.stdout = save
        etype, evalue, etrace = sys.exc_info()
        ename = evalue.__class__.__name__
        emsg = str(evalue)
        #elineno, eline = get_exception_line(st_module, etrace)
        output(msgs.get_msg(ename, lang, default="GenericErrorMsg"), Codes.ERROR, 
            ename=ename, emsg=emsg, inputs=presenter(inputs)
        )
        if inputs:
            output(msgs.get_msg("PrintInputVector", lang), Codes.DEBUG, inputs=presenter(inputs))
    else:
        sys.stdout = save
        if not allow_output and o.content:
            output(msgs.get_msg("DisallowedOutput", lang), Codes.ERROR, output=o.content)
        elif not hide_output:
            output(msgs.get_msg("PrintStudentOutput", lang), Codes.DEBUG, output=o.content)
            
        return st_module
    """