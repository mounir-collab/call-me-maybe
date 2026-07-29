from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from llm_sdk import Small_LLM_Model
from rich.markup import escape


class DecoderUI:
    """Display the current prompt and generated JSON in a live terminal UI."""
    def __init__(self) -> None:
        """Initialize the terminal layout."""
        self.layout: Layout = Layout()

        self.layout.split_column(
            Layout(name="prompt", size=5),
            Layout(name="json", size=12),
        )

        self.prompt: str = ""
        self.json: str = ""

    def set_prompt(self, prompt: str) -> None:
        """Update the displayed prompt."""
        self.prompt = prompt

    def update_json(self, text: str) -> None:
        """Update the displayed JSON output."""
        self.json = text

    def render(self) -> Layout:
        """Render the current UI layout."""
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
        """Clear the displayed prompt and JSON."""
        self.prompt = ""
        self.json = ""


class DecoderContext:
    """Manage live updates during constrained decoding."""
    def __init__(self, model: Small_LLM_Model,
                 ui: DecoderUI, live: Live) -> None:
        """Initialize the decoding context."""
        self.model: Small_LLM_Model = model
        self.ui: DecoderUI = ui
        self.live: Live = live

    def refresh(self, res: list[int]) -> None:
        """Refresh the live UI with the current decoding output."""
        self.ui.update_json(self.model.decode(res))
        self.live.update(self.ui.render())
