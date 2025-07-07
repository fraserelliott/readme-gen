from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input


class HorizontalLayoutExample(App):
    CSS_PATH = "horizontal_layout.tcss"

    def compose(self) -> ComposeResult:
        with Vertical(classes="box"):
            yield Input(placeholder="{project_title}", id="project_name")
            yield Input(placeholder="{author}", id="author")
        
        yield Static("# [red]{project_title}[/red]\n\n## Author: [red]{author}[/red]", classes="box")


if __name__ == "__main__":
    app = HorizontalLayoutExample()
    app.run()