
from src.models import FunctionDefinition





ja = {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  }

a = FunctionDefinition(**ja)
for  param_name , param_def in a.parameters.items() :
    # print(a.parameters.items())
    print(param_name)
    print(param_def)