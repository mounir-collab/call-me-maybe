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
#         generation: List = []
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

    if param_type == "number":
        allowed_chars = set("0123456789.-,}")

        for token_id in range(vocab_size):
            text = model.decode([token_id])

            if text and all(c in allowed_chars for c in text):
                allowed.append(token_id)

    elif param_type == "string":

        for token_id in range(vocab_size):
            text = model.decode([token_id])

            if (
                text
                and '"' not in text
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

def get_params(
    res: list[int],
    model: Small_LLM_Model,
    system_prompt_ids: list[int],
    function: FunctionDefinition,
):
    for index, (param_name, param_def) in enumerate(
        function.parameters.items()
    ):

        if index == 0:
            prefix = f'"{param_name}":'
        else:
            prefix = f',"{param_name}":'

        prefix_ids = model.encode(
            prefix
        )[0].tolist()

        res.extend(prefix_ids)
        system_prompt_ids.extend(prefix_ids)

        allowed_tokens = get_allowed_tokens(
            model,
            param_def.type
        )

        while True:

            logits = model.get_logits_from_input_ids(
                system_prompt_ids
            )

            next_token = max(
                allowed_tokens,
                key=lambda token: logits[token]
            )

            decoded = model.decode([next_token])

            if "," in decoded or "}" in decoded:

                if decoded == "}":
                    system_prompt_ids.append(next_token)
                    res.append(next_token)

                break

            system_prompt_ids.append(next_token)
            res.append(next_token)