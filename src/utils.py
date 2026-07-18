
from llm_sdk import Small_LLM_Model


def get_fn_name(res , model , system_prompt_ids , lst_fn_names_ids , lst_fn_names):
    for index in range(20):
        # fn_name : str = ""
        logits = model.get_logits_from_input_ids(system_prompt_ids)
        new_list = [sublist[index] for sublist in lst_fn_names_ids]
        next_token = max(new_list, key=lambda x: logits[x])
        res.append(next_token)
        system_prompt_ids.append(next_token)
        if fn_name in lst_fn_names :
            break