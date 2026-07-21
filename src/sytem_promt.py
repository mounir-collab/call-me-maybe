# from typing import List

# from .models import FunctionDefinition

# def build_system_prompt(
#     model,
#     lst_functions: list[FunctionDefinition]
# ) -> list[int]:
#     prompt_parts = [
#         "You can call the following functions.",
#         "When a function is needed, respond with a JSON object in this format:",
#         """
# {
#     "prompt": "<user request>",
#     "name": "<function name>",
#     "parameters": {
#         ...
#     }
# }
# """,
#         "",
#         "Available functions:"
#     ]

#     for func in lst_functions:
#         prompt_parts.append(f"\nFunction: {func.name}")
#         prompt_parts.append(f"Description: {func.description}")

#         if func.parameters:
#             prompt_parts.append("Parameters:")
#             for name, param in func.parameters.items():
#                 prompt_parts.append(
#                     f"  - {name}: {param}"
#                 )

#         prompt_parts.append(f"Returns: {func.returns}")

#     system_prompt = "\n".join(prompt_parts)

#     # Adjust depending on your tokenizer API
#     return model.encode(system_prompt)[0].tolist()
#     # return system_prompt

from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition


def build_system_prompt(
    model: Small_LLM_Model,
    lst_functions: list[FunctionDefinition]
) -> list[int]:

    functions_desc = []

    for fn in lst_functions:
        params = ", ".join(
            f"{name}:{param.type}"
            for name, param in fn.parameters.items()
        )

        functions_desc.append(
            f"{fn.name}({params}) -> {fn.returns.type}"
        )

    system_prompt = f"""
Role:
You are a function-calling AI.

Task:
Select the best function and extract its parameters from the user prompt.

Constraints:
- Use only the available functions.
- Do not invent parameters.
- Extract parameter values from the prompt.
- Return exactly one function call.

Format:
{{
"prompt":"<user prompt>",
"name":"<function name>",
"parameters":{{...}}
}}

Available functions:
{chr(10).join(functions_desc)}

Examples:

{{
"prompt":"What is the sum of 2 and 3?",
"name":"fn_add_numbers",
"parameters":{{"a":2.0,"b":3.0}}
}}

{{
"prompt":"Reverse the string 'hello'",
"name":"fn_reverse_string",
"parameters":{{"s":'hello'}}
}}
""".strip()

    return model.encode(system_prompt)[0].tolist()