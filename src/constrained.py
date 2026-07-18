
from llm_sdk import Small_LLM_Model

def get_fn_name(res , model , system_prompt_ids , lst_fn_names_ids , lst_fn_names):
    pass

def get_params(res ):
    pass


def constrained_decoding(prompt , model : Small_LLM_Model , system_prompt_ids, lst_fn_names_ids, lst_fn_names):
    res : list[int] = []
    
    var1 = '{' + f'\n "prompt": "{prompt}",\n "name": "'
    # print(var1)
    var1_ids = model.encode(var1)[0].tolist()
    res.append(var1_ids)
    # print(res, "\n\n\n\n\n\n\n\n\n\n\n\n")
    system_prompt_ids.extend(var1_ids)


    get_fn_name(res , model , system_prompt_ids , lst_fn_names_ids , lst_fn_names)
    print(model.decode(res))
    import sys
    sys.exit(0)


    # var2 : str =  f'",\n "parameters": '
    # var2_ids = model.encode(var2)

    # res.append(var2_ids)
    # system_prompt_ids.extend(var2_ids)


    # get_params(res , system_prompt_ids )

    # var3 : str = "\n}"

    # var3_ids : list[int] = model.encode(var3)

    # res.append(var3_ids)

    return (model.decode(res))


    # prompt 