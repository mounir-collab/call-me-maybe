from pydantic import BaseModel





class FunctionParms(BaseModel):
    type : str

class ReturnFunc(BaseModel):
    type : str


class FunctionDefinition (BaseModel) :
    name : str
    description : str
    parameters : dict[str , FunctionParms]
    returns : ReturnFunc
    
class TestPrompt(BaseModel):
    prompt : str
