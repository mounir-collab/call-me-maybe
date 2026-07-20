from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition

# def get_fn_name(res , model: Small_LLM_Model , system_prompt_ids , lst_fn_names_ids , lst_fn_names):
#     fn_name : str = ""
#     for index in range(20):
#         logits = model.get_logits_from_input_ids(system_prompt_ids)
#         new_list = [sublist[index] for sublist in lst_fn_names_ids]
#         next_token = max(new_list, key=lambda x: logits[x])
#         # fn_name += model.decode(next_token)[0]
#         res.append(next_token)
#         system_prompt_ids.append(next_token)
#         if fn_name in lst_fn_names :
#             break


def get_fn_name(
    res,
    model,
    system_prompt_ids,
    lst_fn_names_ids,
    lst_fn
) -> str:
    fn_name = ""

    # print(model.decode(res)[0])
    # exit(0)

    for index in range(20):

        logits = model.get_logits_from_input_ids(
            system_prompt_ids
        )

        candidates = [
            sublist[index]
            for sublist in lst_fn_names_ids
            if len(sublist) > index
        ]

        if not candidates:
            break

        next_token = max(
            candidates,
            key=lambda token: logits[token]
        )

        fn_name += model.decode(next_token)

        res.append(next_token)
        # print(model.decode(next_token))
        system_prompt_ids.append(next_token)

        # print(fn_name)
        
        # print(res)
        # print(model.decode(res)[0])
        # exit(0)
        # if f.name in lst_fn:
        #     return f.name
        if fn_name in [f.name for f in lst_fn]:
            return fn_name 

    # print(fn_name)
    return fn_name

# res
def get_params(function : FunctionDefinition , model : Small_LLM_Model ):
    
    res : list[int] = []

    var1 : str =  '"parameters": {'
    var1_ids = model.encode(var1)[0].tolist()

    fn_name = function.name
    
    for param_name , param_type in function.parameters.items() :
        
        if param_type.type == "integer":
            pass
        elif param_type.type == "float":
            pass
        elif param_type.type == "number":
            pass
        elif param_type.type == "string":
            pass
        elif param_type.type == "boolean":
            pass
