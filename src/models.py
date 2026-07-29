from pydantic import BaseModel, Field


class FunctionParms(BaseModel):
    """Represent the type of a function parameter."""
    type: str


class ReturnFunc(BaseModel):
    """Represent the return type of a function."""
    type: str


class FunctionDefinition(BaseModel):
    """Define a callable function and its schema."""
    name: str
    description: str
    parameters: dict[str, FunctionParms]
    returns: ReturnFunc


class TestPrompt(BaseModel):
    """Represent a user prompt used for testing."""
    prompt: str = Field(min_length=1)
