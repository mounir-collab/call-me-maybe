from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from llm_sdk import Small_LLM_Model
from rich.markup import escape


class DecoderUI:

    def __init__(self) -> None:

        self.layout: Layout = Layout()

        self.layout.split_column(
            Layout(name="prompt", size=5),
            Layout(name="json", size=12),
        )

        self.prompt: str = ""
        self.json: str = ""

    def set_prompt(self, prompt: str) -> None:
        self.prompt = prompt

    def update_json(self, text: str) -> None:
        self.json = text

    def render(self) -> Layout:

        self.layout["prompt"].update(
            Panel(
                self.prompt,
                title="🤖 Current Prompt",
                border_style="cyan",
            )
        )

        self.layout["json"].update(
            Panel(
                escape(self.json),
                title="📄 Generated JSON",
                border_style="green",
            )
        )

        return self.layout

    def reset(self) -> None:
        self.prompt = ""
        self.json = ""


class DecoderContext:

    def __init__(self, model: Small_LLM_Model,
                 ui: DecoderUI, live: Live) -> None:
        self.model: Small_LLM_Model = model
        self.ui: DecoderUI = ui
        self.live: Live = live

    def refresh(self, res: list[int]) -> None:
        self.ui.update_json(self.model.decode(res))
        self.live.update(self.ui.render())
