from llm_sdk import Small_LLM_Model
from .utils import get_fn_name
from .models import TestPrompt , FunctionDefinition
from .params import get_params
import json
from .ui import DecoderContext
import time 
def constrained_decoding(prompt : TestPrompt , model : Small_LLM_Model , system_prompt_ids, lst_fn_names_ids, lst_fn , ui , live):
    res : list[int] = []
    
    context = DecoderContext(model, ui, live)

    escaped_prompt = json.dumps(prompt.prompt)
    var1 = (
        "{"
        f'\n "prompt": {escaped_prompt},'
        '\n "name": "'
    )
    # print(var1)
    var1_ids = model.encode(var1)[0].tolist()
    res.extend(var1_ids)
    system_prompt_ids.extend(var1_ids)

    context.refresh(res)

    # print(res)
    lst_fn_names = [fn.name for fn in lst_fn]
    fn_name = get_fn_name(res , model , system_prompt_ids , lst_fn_names_ids , lst_fn , context)
    # print(fn_name)
    # if (not fn_name or not fn_name in lst_fn_names ):
    #     pass
    fn_def : FunctionDefinition = [fn for fn in lst_fn if fn.name == fn_name][0]
    # print(fn_def.name)
    # exit(0)
    # print(res)
    # print(name)
    # print(model.decode(res)[0])
    # print(res)
    # import sys
    # sys.exit(0)


    var2 : str =  f'",\n "parameters": ' + '{'
    var2_ids = model.encode(var2)[0].tolist()

    res.extend(var2_ids)
    system_prompt_ids.extend(var2_ids)

    context.refresh(res)

    get_params(res , model , system_prompt_ids , fn_def , context)

    brace_ids = model.encode("\n  }")[0].tolist()
    system_prompt_ids.extend(model.encode("\n  }")[0])
    res.extend(model.encode("\n  }")[0])

    context.refresh(res)

    var3 : str = "\n}"

    var3_ids : list[int] = model.encode(var3)[0].tolist()

    system_prompt_ids.extend(var3_ids)
    res.extend(var3_ids)
    # exit(0)
    # print(model.decode(res))
    # print("".join(item) )
    # exit(0)

    context.refresh(res)
    time.sleep(1)
    return ("".join(model.decode(res)))
    # print(res)
    # print(model.decode(res))
    # print("".join(model.decode(res)))
    # exit(0)


    # prompt 