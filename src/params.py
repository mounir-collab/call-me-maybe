from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition


# #  self.model = model
# #         self.prompt = prompt
# #         self.parameters = parameters
#         # self.param_keys = list(self.parameters.keys())

# def generate_arguments(self) -> dict[str, Any]:
#         """
#         Generate parameters using constrained decoding.
#         Returns:
#             dict: Generated parameters as a dictionary,
#             or an empty dict if decoding fails.
#         """
#         generation: list = []
#         input_ids = self.model.encode(self.prompt).squeeze().tolist()
#         for index, key in enumerate(self.param_keys):
#             if index == 0:
#                 structure_str = '{"' + key + '":'
#             else:
#                 structure_str = ',"' + key + '":'
#             enc_tokens = self.model.encode(structure_str).squeeze().tolist()
#             generation = generation + enc_tokens
#             input_ids = input_ids + enc_tokens
#             param_type = self.parameters[key].type
#             if param_type == "number":
#                 allowed_chars = "0123456789.,}"
#             elif param_type == "string":
#                 not_allowed_chars = "\n\""
#             else:
#                 allowed_chars = ""

#             while True:
#                 logits = self.model.get_logits_from_input_ids(input_ids)
#                 for token_id in range(len(logits)):
#                     token_char = self.model.decode([token_id])
#                     if param_type == "number":
#                         if not (token_char and all(c in allowed_chars
#                                                    for c in token_char)):
#                             logits[token_id] = float("-inf")
#                     elif param_type == "string":
#                         if (token_char and all(c in not_allowed_chars
#                                                for c in token_char)):
#                             logits[token_id] = float("-inf")
#                 id = np.argmax(logits)
#                 char_now = self.model.decode([id])
#                 if ',' in char_now or '}' in char_now:
#                     if param_type == "string" and '"' in char_now:
#                         if ")" in char_now:
#                             quote_id = self.model.encode(
#                                 ')').squeeze().tolist()
#                             generation.append(quote_id)
#                             input_ids.append(quote_id)
#                         quote_id = self.model.encode('"').squeeze().tolist()
#                         generation.append(quote_id)
#                         input_ids.append(quote_id)
#                     break
#                 generation.append(id)
#                 input_ids.append(id)
#         end_char = self.model.encode("}").squeeze().tolist()
#         generation.append(end_char)
#         result_str = self.model.decode(generation)
#         try:
#             data: dict[str, Any] = json.loads(result_str)
#         except Exception:
#             return {}
#         for key in data:
#             if isinstance(data[key], int):
#                 data[key] = float(data[key])

#         return data



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

    elif param_type == "boolean":

        for token_id in range(vocab_size):
            text = model.decode([token_id])

            if text in (
                "true",
                "false",
                ",",
                "}"
            ):
                allowed.append(token_id)

    return allowed

def get_number_param(model : Small_LLM_Model, system_prompt_ids , param_def):
    allowed_tokens = get_allowed_tokens(
            model,
            param_def.type
        )
    
    float_tokens = []
    number = ""
    while True:

            logits = model.get_logits_from_input_ids(
                system_prompt_ids
            )
            
            next_token = max(
                allowed_tokens,
                key=lambda token: logits[token]
            )
            print(model.decode(next_token))
            # if model.decode(next_token) == " //":
            #     break
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

    
    

# def get_bool_param(model , system_prompt_ids , param_def , function):
#     allowed_tokens = get_allowed_tokens(
#             model,
#             param_def.type
#         )
    
#     while True:

#             logits = model.get_logits_from_input_ids(
#                 system_prompt_ids
#             )
            
#             next_token = max(
#                 allowed_tokens,
#                 key=lambda token: logits[token]
#             )
#             print(model.decode(next_token))
#             if model.decode(next_token) == " //":
#                 break
#             decoded = model.decode([next_token])
#             if "," in decoded or "}" in decoded:
#                 break


#     number = str(float(float_str))
#     normalized_ids = model.encode(number)[0]

#     return normalized_ids

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
        print(decoded)
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

        # allowed_tokens = get_allowed_tokens(
        #     model,
        #     param_def.type
        # )

        # while True:

        #     logits = model.get_logits_from_input_ids(
        #         system_prompt_ids
        #     )
            

        #     next_token = max(
        #         allowed_tokens,
        #         key=lambda token: logits[token]
        #     )
        #     print(model.decode(next_token))
        #     # if any(c in model.decode(next_token) for c in ['/', '#' , '`']) :
        #     #     break
        #     if model.decode(next_token) == " //":
        #         break
        #     decoded = model.decode([next_token])
        #     # if decoded == "'" and param_def.type == "string":
        #     #     next_token = model.encode('"')[0].tolist()
        #     #     system_prompt_ids.extend(next_token)
        #     #     res.extend(next_token)
        #     #     continue
        #     if "," in decoded or "}" in decoded:

        #         if param_def.type == "string" and "," in decoded :
        #             system_prompt_ids.append(model.encode('"')[0])
        #             res.append(model.encode('"')[0])
        #         break
            
        #     system_prompt_ids.append(next_token)
        #     res.append(next_token)

        if param_def.type == "number":
            my_result = get_number_param(model , system_prompt_ids , param_def)
            res.extend(my_result)
        
        elif param_def.type == "integer" :
            my_result = get_number_param(model , system_prompt_ids , param_def)
            res.extend(my_result)

        elif param_def.type == "boolean":
            pass
        elif param_def.type == "string" :
            my_result = get_str_param(model , system_prompt_ids , param_def)
            res.extend(my_result)
        