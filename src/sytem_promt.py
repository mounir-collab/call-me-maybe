from typing import List

from .models import FunctionDefinition

def build_system_prompt(
    model,
    lst_functions: list[FunctionDefinition]
) -> list[int]:
    prompt_parts = [
        "You can call the following functions.",
        "When a function is needed, respond with a JSON object in this format:",
        """
{
    "prompt": "<user request>",
    "name": "<function name>",
    "parameters": {
        ...
    }
}
""",
        "",
        "Available functions:"
    ]

    for func in lst_functions:
        prompt_parts.append(f"\nFunction: {func.name}")
        prompt_parts.append(f"Description: {func.description}")

        if func.parameters:
            prompt_parts.append("Parameters:")
            for name, param in func.parameters.items():
                prompt_parts.append(
                    f"  - {name}: {param}"
                )

        prompt_parts.append(f"Returns: {func.returns}")

    system_prompt = "\n".join(prompt_parts)

    # Adjust depending on your tokenizer API
    return model.encode(system_prompt)[0].tolist()
    # return system_prompt