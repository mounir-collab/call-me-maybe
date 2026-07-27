from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition
import time


def get_allowed_tokens(model: Small_LLM_Model, param_type: str) -> list[int]:
    allowed = []

    vocab_size = len(
        model.get_logits_from_input_ids([0])
    )
    # INTEGER TO ADD
    if param_type == "number":
        allowed_chars = set("-0123456.789,}")

        for token_id in range(vocab_size):
            text = model.decode([token_id])

            if text and all(c in allowed_chars for c in text):
                allowed.append(token_id)
    if param_type == "integer":
        allowed_chars = set("0123456789},")

        for token_id in range(vocab_size):
            text = model.decode([token_id])

            if text and all(c in allowed_chars for c in text):
                allowed.append(token_id)

    elif param_type == "string":

        for token_id in range(vocab_size):
            text = model.decode([token_id])

            if (
                text
                # and '"' not in text
                and '\n' not in text
            ):
                allowed.append(token_id)

    return allowed

def get_number_param(model : Small_LLM_Model, system_prompt_ids , param_def ):
    allowed_tokens = get_allowed_tokens(
            model,
            param_def.type
        )
    
    float_tokens = []
    number = ""
    max_tokens = 0
    while True:
            if (max_tokens == 32):
                break
            logits = model.get_logits_from_input_ids(
                system_prompt_ids
            )
            
            next_token = max(
                allowed_tokens,
                key=lambda token: logits[token]
            )
            max_tokens+=1
            decoded = model.decode([next_token])
            if "," in decoded or "}" in decoded:
                break
            float_tokens.append(next_token)
            system_prompt_ids.append(next_token)
    float_str = model.decode(float_tokens)
    normalized_ids = model.encode(float_str)[0].tolist()

    if param_def.type in ("number" , "float"):
        number = str(float(float_str))
        normalized_ids = model.encode(number)[0].tolist()
        return normalized_ids
    return normalized_ids

def get_str_param(
    model: Small_LLM_Model,
    system_prompt_ids: list[int],
    param_def,
) -> list[int]:

    allowed_tokens = get_allowed_tokens(model, param_def.type)

    result = []

    MAX_TOKENS = 100

    for _ in range(MAX_TOKENS):

        logits = model.get_logits_from_input_ids(system_prompt_ids)

        next_token = max(
            allowed_tokens,
            key=lambda t: logits[t]
        )

        decoded = model.decode([next_token])
        # Did we reach the closing quote?
        if '"' in decoded:

            before = decoded.split('"')[0]
            if before:
                ids = model.encode(before)[0].tolist()
                result.extend(ids)
                system_prompt_ids.extend(ids)

            break

        result.append(next_token)
        system_prompt_ids.append(next_token)

    else:
        raise RuntimeError("String decoding exceeded limit.")

    # Close the string ourselves.
    quote = model.encode('"')[0].tolist()

    result.extend(quote)
    system_prompt_ids.extend(quote)

    return result


def get_params(
    res: list[int],
    model: Small_LLM_Model,
    system_prompt_ids: list[int],
    function: FunctionDefinition,
    context
):  
    for index, (param_name, param_def) in enumerate(
        function.parameters.items()
    ):
        mumber_tokens = []
        if index == 0:
            prefix = '\n   "'+ f'{param_name}": '
            if param_def.type == "string":
                prefix = '\n   "'+ f'{param_name}": "'
        else:
            prefix = f',' + "\n   " + f'"{param_name}": '
            if param_def.type == "string":
                prefix = f',' + "\n   " + f'"{param_name}": "'

        prefix_ids = model.encode(
            prefix
        )[0].tolist()

        res.extend(prefix_ids)
        system_prompt_ids.extend(prefix_ids)

        if param_def.type == "number":
            my_result = get_number_param(model , system_prompt_ids , param_def)
            res.extend(my_result)
            context.refresh(res)
            time.sleep(0.5)
        
        elif param_def.type == "integer" :
            my_result = get_number_param(model , system_prompt_ids , param_def)
            res.extend(my_result)
            context.refresh(res)
            time.sleep(0.5)
            
        elif param_def.type == "string" :
            my_result = get_str_param(model , system_prompt_ids , param_def)
            res.extend(my_result)
            context.refresh(res)
            time.sleep(0.5)
        