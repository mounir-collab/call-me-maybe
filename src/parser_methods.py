import json
from .models import FunctionDefinition, TestPrompt
from pydantic import ValidationError
from typing import Any


class InputFileError(Exception):
    """This for raising error when a file is missing or invalid"""


def load_func_def(path: str) -> list[FunctionDefinition]:
    """load and validate the function definitions file"""

    try:
        with open(path, mode="r") as f:
            content: list[dict[str, Any]] | object = json.load(f)
            if not isinstance(content, list):
                raise InputFileError(
                    "The json file should be a list of dict !!!"
                    )
    except FileNotFoundError:
        raise InputFileError(
            f"Functions definition file not found: {path}"
            )
    except json.JSONDecodeError as e:
        raise InputFileError(f"Invalid JSON in {path}: {e}")

    try:
        ft_none_data: dict[str, Any] = {
            "name": "ft_none",
            "description": "...",
            "parameters": {},
            "returns": {"type": "null"},
        }
        ft_none = FunctionDefinition(**ft_none_data)
        return [FunctionDefinition(**item) for item in content] + [ft_none]
    except ValidationError as e:
        raise InputFileError(
            f"Invalid function definition schema in {path}: {e}"
        )


def load_test_promts(path: str) -> list[TestPrompt]:
    """this is for loading the json code from the input and validate it"""
    try:
        with open(path, "r") as f:
            content: list[dict[str, Any]] | object = json.load(f)
            if not isinstance(content, list):
                raise InputFileError(
                    "The json file should be a list of dict !!!"
                    )
    except FileNotFoundError:
        raise InputFileError(f"Test prompts file not found: {path}")
    except json.JSONDecodeError as e:
        raise InputFileError(f"Invalid JSON in {path}: {e}")

    try:
        return [TestPrompt(**item) for item in content]
    except ValidationError as e:
        print(e.errors())
        for error in e.errors():
            pass
        raise InputFileError(
            f"Invalid test prompt schema in {path}: {e}"
            )
