from pydantic import BaseModel
from src.models import FunctionDefinition , ReturnFunc , FunctionParms
from llm_sdk import Small_LLM_Model 




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

# class a(BaseModel) :
#   prompt : str
#   arb : int

#   # def __str__(self):
#   #   return 

# res = a(prompt = "hs" , arb = 3)
# print(res)

# class b :
#   a : int = 1
#   b : int = 3

# c = b
# print(c)

# my_prompt = "whatisthesumofprimenumbersbetween1and10?"
# model = Small_LLM_Model()


# lst_ids = model.encode(my_prompt)[0].tolist()

# print(lst_ids)
# # lo = max(lst_ids,key= lambda x: model.get_logits_from_input_ids(lst_ids)[x])

# # text = model.decode(lo)
# # print(text)

# print(model.get_logits_from_input_ids(lst_ids))


# # print(len(lst_ids)) 

