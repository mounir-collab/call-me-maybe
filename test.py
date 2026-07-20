from pydantic import BaseModel
# from src.models import FunctionDefinition , ReturnFunc , FunctionParms
# from llm_sdk import Small_LLM_Model 




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



# # dicti = {
# #     "last_name" : "add" ,
# #     "first_name" : "aq"
# # }

# a = arobas( first_name = "az", last_name =  "ss")
# print(a["first_name"])
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

# my_prompt = "what is the sum of prime numbers between 1 and 10?"
# model = Small_LLM_Model()


# lst_ids = model.encode(my_prompt)[0].tolist()

# # print(lst_ids)
# # lo = max(lst_ids,key= lambda x: model.get_logits_from_input_ids(lst_ids)[x])

# # text = model.decode(lo)
# # print(text)
# import numpy as np
# logits = model.get_logits_from_input_ids(lst_ids)
# print(model.decode(np.argmax(logits)))


# print(len(lst_ids)) 


# a = [ 1 , 2 , 3]
# b = [4 , 5]

# c = a.extend(b)

# print(c)

# a.append(b)
# print(a)
# a.extend(b)
# print(a)


# a = 10 

# a = 10
# print(id(a))
# a = 2
# print(id(a))
# b = [1 , 2]


# def do(d):
#     d.append(1)

# def add(a):
#     a+=1


# add(a)

# # add()

# do(b)
# print(a)
# print(b)


# a = [1 , 2 , 3]

# b = [4]

# print(a + b)


d = {
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

print(d["parameters"].items())
# for x_name , y_type in d["parameters"].items() :
#     print(x_name)
#     print(y_type)


for index , (param_name , param_def) in enumerate(d["parameters"].items() , 0) :
    print(index)
    print(param_name)
    print(param_def)