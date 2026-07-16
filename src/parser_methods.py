
import json 
from .models import FunctionDefinition , TestPrompt
from pydantic import ValidationError


class InputFileError(Exception):
    """ This for raising error when a file is missing or invalid """
    

def load_func_def(path : str) :
    """ load and validate the function definitions file """

    try:
        with open(path , mode= 'r') as f:
            content = json.load(f)
            if not isinstance(content , list):
                raise InputFileError("The json file should be a list of dict !!!")
    except FileNotFoundError as e:
        raise InputFileError(f"Functions definition file not found: {path}") from e
    except json.JSONDecodeError as e :
        raise InputFileError(f"Invalid JSON in {path}: {e}") from e

    try :
        return [FunctionDefinition(**item) for item in content ]
    except ValidationError as e:
        raise InputFileError(f"Invalid function definition schema in {path}: {e}") from e
    except Exception as e :
        raise e 


def load_test_promts(path : str) :
    """ this is for loading the json code from the input and validate it """
    try :
        with open(path , 'r') as f :
            content = json.load(f)
            if not isinstance(content , list):
                raise InputFileError("The json file should be a list of dict !!!")
    except FileNotFoundError as e:
        raise InputFileError(f"Test prompts file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise InputFileError(f"Invalid JSON in {path}: {e}") from e
    
    try :
        return [TestPrompt(**item) for item in content]
    except ValidationError as e:
        raise InputFileError(f"Invalid test prompt schema in {path}: {e}") from e