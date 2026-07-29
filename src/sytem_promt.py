from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition
from typing import Any


def build_system_prompt(
    model: Small_LLM_Model,
    lst_functions: list[FunctionDefinition]
) -> Any:
    """Build and encode the system prompt for constrained function calling."""
    prompt: list[str] = []

    prompt.append("You are a function calling assistant.")
    prompt.append("Choose exactly one function.")
    prompt.append("Extract every parameter exactly from the user prompt.")
    prompt.append("Never invent functions or parameters.")
    prompt.append("Copy strings exactly.")
    prompt.append(
        "Keep file paths, SQL queries, regexes and templates unchanged."
        )
    prompt.append("Return only a JSON object.")
    prompt.append("")
    prompt.append("Available functions:")

    for fn in lst_functions:

        params: str = ", ".join(
            f"{name}:{param.type}"
            for name, param in fn.parameters.items()
        )

        prompt.append(
            f"- {fn.name}({params})"
        )

        if fn.description:
            prompt.append(
                f"  Description: {fn.description}"
            )

    prompt.append("")
    prompt.append("Example:")
    prompt.append(
        """
    {
        "prompt": "Reverse the string 'hello'",
        "name": "fn_reverse_string",
        "parameters": {
            "s": "hello"
        }
    }
    """
    )

    system_prompt: str = "\n".join(prompt)

    return model.encode(system_prompt)[0].tolist()
