from rich.layout import Layout
from rich import print
from rich.panel import Panel





test_layout = Layout()
test_layout.split_column(
    Layout(name = "hold"),
    Layout(name = "hj")
)

# print(type(test_layout))
test_layout["hold"].update(
    Panel(
        "hello",
        title = "main",
        border_style = "cyan"
    )
)

print(test_layout)