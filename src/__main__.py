import os
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from .ui import DecoderUI

import argparse
# from pathlib import Path
import sys
from .parser_methods import load_func_def , load_test_promts
from llm_sdk import Small_LLM_Model
from .vocab import load_vocab
from .sytem_promt import build_system_prompt
from .constrained import constrained_decoding
import time
from .models import FunctionDefinition

load_dotenv()
# HF_TOKEN = os.getenv("HF_TOKEN")
# print(HF_TOKEN)

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


import json

def main() -> None:
    os.system("clear")
    print("⚙️  Initializing Call Me Maybe...\n")
    start = time.time()
    ob_args = parse_args()
    # print(ob_args.__dict__)
    # print(ob_args.functions_definition)
    output : list [str] = []

    # try :
    print("📂 Loading function definitions...")
    functions : list[FunctionDefinition] = load_func_def("data/input/functions_definition.json")
    print(f"✔️  {len(functions)} function definitions loaded.")
    print("📝 Loading test prompts...")
    prompts = load_test_promts("data/input/function_calling_tests.json")
    print(f"✔️  {len(prompts)} prompts loaded.")

    # fn = functions[0]

    # fn.parameters
    # ad = fn.parameters.items()
    # for name_param , type_param in ad :
    #     print(name_param)
    #     print(type_param.type)
    
    # print(ad)
    # exit(0)
    # print(functions)
    # print(function)
    # print(sys.path[0])
    print("🧠 Loading language model...")
    model  = Small_LLM_Model()
    print("✔️  Language model ready.")
    # print(model.get_path_to_vocab_file())
    # for function in functions :
    #     print(function)
    # for pr in prompts :
    #     print(pr)
    # print(prompts)

    # with open("test.json" , 'w') as f :
    #     json.dump(load_vocab(model.get_path_to_vocab_file()) , f)

    # print(build_system_prompt(model , functions))

    system_prompt_ids = build_system_prompt(model , functions)
    # system_prompt = build_system_prompt(functions)
    # system_prompt_ids = model.encode(system_prompt)[0].tolist()
    # print(model.decode(system_prompt_ids))
    # exit(0)
    # system_prompt_ids = []
    # print(type(functions), type(functions[0]))
    # lst_fn_names : list[str] = [f.name for f in functions] + ["ft_none"]
    # lst_fn_names_ids : list[int]= [model.encode(fn.name)[0].tolist() for fn in functions]
    lst_fn_names_ids: list[list[int]] = [model.encode(fn.name)[0].tolist() for fn in functions]

    # print(lst_fn_names)
    # print(lst_fn_names_ids)
    
    # print(prompts)
    os.makedirs(os.path.dirname(ob_args.output), exist_ok=True)
    print("\n🚀 Starting constrained decoding...\n")
    ui = DecoderUI()
    console = Console()

    with open(ob_args.output , 'w') as f :
        f.write("[\n")
        f.flush()
            # user_prompt_ids = model.encode(prompt)[0].tolist()
            # input_ids = (
            #     system_prompt_ids +
            #     user_prompt_ids
            # )
            # res: str = constrained_decoding(prompt, model, system_prompt_ids, lst_fn_names_ids, functions)
            # print(res)
            # console.clear()
            # ui.reset()                 # clear previous JSON

        with Live(
            ui.render(),
            refresh_per_second=30,
            transient=True,
        ) as live:

            for i , prompt in enumerate(prompts) :
                # ui.reset()                  # clear previous JSON
                ui.set_prompt(prompt.prompt)
                # live.update(ui.render())

                res = constrained_decoding(
                    prompt,
                    model,
                    system_prompt_ids,
                    lst_fn_names_ids,
                    functions,
                    ui,
                    live,
                )
                ob = json.loads(res)
                json.dump(ob ,f , indent=2)
                f.flush()
                if i < len(prompts) - 1:
                    f.write(",\n")
                # if (i == len(prompts) - 1) :
                #     ui.reset()
                    # console.clear()
                f.flush()
            # print()
            ui.reset()
            live.update(ui.render(), refresh=True)
            live.stop()
        f.write("\n]")
        # output.append(res)
        # input_ids , lst_fn_names , lst_ids_fn , Functions definitions , prompt
    # ui.reset()                   # clear previous JSON
    # console.clear()
    end = time.time()
    # print("the time is : " , end - start)
    # print("time in min is : " , (end - start) / 60)
    elapsed = end - start

    console.print(
    Panel(
        f"""[bold green]✔ Finished[/]

        🕒 Execution Time : [cyan]{elapsed:.3f} seconds[/]
        🕒 Minutes       : [yellow]{elapsed / 60:.3f} min[/]
        """,
        title="Statistics",
        border_style="green",
        expand=False,
        )
    )
    # except Exception as e:
    #     print(e)


if __name__ == "__main__":
    main()