
from src.models import FunctionDefinition , TestPrompt
from pydantic import ValidationError




ja = {
}

try :
   a = TestPrompt(**ja)
except ValidationError as e :
    print(e)