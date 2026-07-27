from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel



class DecoderUI:

    def __init__(self):

        self.layout = Layout()

        self.layout.split_column(
            Layout(name="prompt", size=5),
            Layout(name="json" , size = 12),
        )

        self.prompt = ""
        self.json = ""

    def set_prompt(self, prompt: str):
        self.prompt = prompt

    def update_json(self, text: str):
        self.json = text

    def render(self):

        self.layout["prompt"].update(
            Panel(
                self.prompt,
                title="🤖 Current Prompt",
                border_style="cyan",
            )
        )

        self.layout["json"].update(
            Panel(
                self.json,
                title="📄 Generated JSON",
                border_style="green",
            )
        )

        return self.layout
    

    def reset(self):
        self.prompt = ""
        self.json = ""

class DecoderContext:

    def __init__(self, model, ui: DecoderUI, live: Live):
        self.model = model
        self.ui = ui
        self.live = live

    def refresh(self, res):
        self.ui.update_json(self.model.decode(res))
        self.live.update(self.ui.render())
