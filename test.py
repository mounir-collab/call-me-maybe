from pydantic import BaseModel
from src.models import FunctionDefinition , ReturnFunc , FunctionParms




# my_dict = {
#     "name": "fn_add_numbers",
#     "description": "Add two numbers together and return their sum.",
#     "parameters": {
#       "a": {
#         "type": "number"
#       },
#       "b": {
#         "type": "number"
#       }
#     },
#     "returns": {
#       "type": "number"
#     }
#   }

# func_def = FunctionDefinition(
#     name="fn_add_numbers",
#     description="Add two numbers together and return their sum.",
#     parameters= {
#         "a": FunctionParms(type="number"),
#         "b": FunctionParms(type="number"),
#     },
#     returns= ReturnFunc(type = "number"),
#     # returns= {"type": "number"}
# )

# class arobas(BaseModel):
#     first_name : str
#     last_name : str



# dicti = {
#     "last_name" : "add" ,
#     "first_name" : "aq"
# }

# a = arobas( "az", last_name =  "ss")
# a = arobas(**dicti)

class a(BaseModel) :
  prompt : str
  arb : int

  # def __str__(self):
  #   return 

res = a(prompt = "hs" , arb = 3)
print(res)

class b :
  a : int = 1
  b : int = 3

c = b
print(c)