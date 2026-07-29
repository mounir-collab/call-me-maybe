from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition
from .ui import DecoderContext


def get_fn_name(
    res: list[int],
    model: Small_LLM_Model,
    system_prompt_ids: list[int],
    lst_fn_names_ids: list[list[int]],
    lst_fn: list[FunctionDefinition],
    context: DecoderContext
) -> str:
    """Select and decode the most likely
    function name from the allowed candidates."""
    fn_name: str = ""

    for index in range(30):

        logits: list[float] = model.get_logits_from_input_ids(
            system_prompt_ids
        )

        candidates: list[int] = [
            sublist[index]
            for sublist in lst_fn_names_ids
            if len(sublist) > index
        ]

        if not candidates:
            break

        next_token: int = max(
            candidates,
            key=lambda token: logits[token]
        )

        fn_name += model.decode(next_token)

        res.append(next_token)
        context.refresh(res)
        system_prompt_ids.append(next_token)

        if fn_name in [f.name for f in lst_fn]:
            return fn_name
    return fn_name
