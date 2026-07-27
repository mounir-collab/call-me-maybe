import os
from dotenv import load_dotenv
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from .ui import DecoderUI

import argparse
import sys
from .parser_methods import load_func_def , load_test_promts
from llm_sdk import Small_LLM_Model
from .vocab import load_vocab
from .sytem_promt import build_system_prompt
from .constrained import constrained_decoding
import time
from .models import FunctionDefinition

load_dotenv()

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

    print("📂 Loading function definitions...")
    functions : list[FunctionDefinition] = load_func_def("data/input/functions_definition.json")
    print(f"✔️  {len(functions)} function definitions loaded.")
    print("📝 Loading test prompts...")
    prompts = load_test_promts("data/input/function_calling_tests.json")
    print(f"✔️  {len(prompts)} prompts loaded.")

    print("🧠 Loading language model...")
    model  = Small_LLM_Model()
    print("✔️  Language model ready.")

    system_prompt_ids = build_system_prompt(model , functions)
    lst_fn_names_ids: list[list[int]] = [model.encode(fn.name)[0].tolist() for fn in functions]

    os.makedirs(os.path.dirname(ob_args.output), exist_ok=True)
    print("\n🚀 Starting constrained decoding...\n")
    ui = DecoderUI()
    console = Console()

    with open(ob_args.output , 'w') as f :
        f.write("[\n")
        f.flush()

        with Live(
            ui.render(),
            refresh_per_second=30,
            transient=False,
        ) as live:

            for i , prompt in enumerate(prompts) :
                ui.set_prompt(prompt.prompt)

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
                # print(res)
                json.dump(ob ,f , indent=2)
                f.flush()
                if i < len(prompts) - 1:
                    f.write(",\n")
                f.flush()
            ui.reset()
            live.update(ui.render(), refresh=True)
        f.write("\n]")
    
    end = time.time()
    elapsed = end - start

    console.print(
    Panel(
        f"""[bold green]✔ Finished[/]

        🕒 Execution Time : [cyan]{elapsed:.3f} seconds[/]
        🕒 Minutes       : [yellow]{elapsed / 60:.3f} min[/]
        """,
        title="Time",
        border_style="green",
        expand=False,
        )
    )

if __name__ == "__main__":
    try :
        main()
    except Exception as e:
        print(e)