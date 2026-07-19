from llm_sdk import Small_LLM_Model
from .utils import get_fn_name
from .models import TestPrompt

# def get_fn_name(res , model , system_prompt_ids , lst_fn_names_ids , lst_fn_names):
#     pass

def get_params(res ):
    pass


def constrained_decoding(prompt : TestPrompt , model : Small_LLM_Model , system_prompt_ids, lst_fn_names_ids, lst_fn):
    res : list[int] = []
    
    var1 = '{' + f'\n "prompt": "{prompt.prompt}",\n "name": "'
    # print(var1)
    var1_ids = model.encode(var1)[0].tolist()
    res.append(var1_ids)
    system_prompt_ids.extend(var1_ids)


    # print(res)
    get_fn_name(res , model , system_prompt_ids , lst_fn_names_ids , lst_fn)
    # print(res)
    # print(name)
    # print(model.decode(res)[0])
    # print(res)
    # import sys
    # sys.exit(0)


    var2 : str =  f'",\n "parameters": '
    var2_ids = model.encode(var2)

    res.append(var2_ids)
    system_prompt_ids.extend(var2_ids)


    get_params(res , system_prompt_ids )

    var3 : str = "\n}"

    var3_ids : list[int] = model.encode(var3)

    res.append(var3_ids)
    # exit(0)
    # print(model.decode(res))
    # print("".join(item) )
    # exit(0)
    return ("".join(model.decode(res)))


    # prompt 