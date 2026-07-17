import argparse
from pathlib import Path
import sys
from .parser_methods import load_func_def , load_test_promts
from llm_sdk import Small_LLM_Model
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        prog="src",
        description= (
        "Translate natural language prompts into structured function calls "
        "using constrained decoding with a small LLM."
        )
        )

    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json"
        )
    
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json"
    )

    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json"
    )
    # support a lot of models for bonus
    parser.add_argument("--model",
        default= "Qwen/Qwen3-0.6B"
    )
    return parser.parse_args()




def main() -> None:

    ob_args = parse_args()
    # print(ob_args.__dict__)
    # print(ob_args.functions_definition)
    
    try :
        functions = load_func_def("data/input/functions_definition.json")
        prompts = load_test_promts("data/input/function_calling_tests.json")
        # print(sys.path[0])
        model  = Small_LLM_Model()
        print(model.get_path_to_vocab_file())
        # for function in functions :
        #     print(function)
        for pr in prompts :
            print(pr)
        # print(prompts)
    except Exception as e:
        print(e)
    pass


if __name__ == "__main__":
    main()