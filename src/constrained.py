from llm_sdk import Small_LLM_Model
from .utils import get_fn_name
from .models import TestPrompt, FunctionDefinition
from .params import get_params
import json
import time
from .ui import DecoderUI, DecoderContext
from rich.live import Live


def constrained_decoding(
    prompt: TestPrompt,
    model: Small_LLM_Model,
    system_prompt_ids: list[int],
    lst_fn_names_ids: list[list[int]],
    lst_fn: list[FunctionDefinition],
    ui: DecoderUI,
    live: Live,
):
    res: list[int] = []

    context: DecoderContext = DecoderContext(model, ui, live)

    escaped_prompt: str = json.dumps(prompt.prompt)
    var1 = "{" f'\n "prompt": {escaped_prompt},' '\n "name": "'

    var1_ids: list[int] = model.encode(var1)[0].tolist()
    res.extend(var1_ids)
    system_prompt_ids.extend(var1_ids)

    context.refresh(res)

    fn_name: str = get_fn_name(
        res, model, system_prompt_ids, lst_fn_names_ids, lst_fn, context
    )
    fn_def: FunctionDefinition = [fn for fn in lst_fn if fn.name == fn_name][0]
    var2: str = '",\n "parameters": ' + "{"
    var2_ids: list[int] = model.encode(var2)[0].tolist()

    res.extend(var2_ids)
    system_prompt_ids.extend(var2_ids)

    context.refresh(res)

    get_params(res, model, system_prompt_ids, fn_def, context)

    brace_ids: list[int] = model.encode("\n  }")[0].tolist()
    system_prompt_ids.extend(brace_ids)
    res.extend(brace_ids)

    context.refresh(res)

    var3: str = "\n}"

    var3_ids: list[int] = model.encode(var3)[0].tolist()

    system_prompt_ids.extend(var3_ids)
    res.extend(var3_ids)

    context.refresh(res)
    time.sleep(1)
    return model.decode(res)
