from merge_tag_inputs import MergeTagInput
import re
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from textual.widgets import Static

#usage: addColor("foo", "red") => "[red]foo[/red]"
def addColor(str, color):
    return f"[{color}]{str}[/{color}]"

class ReadmeGenerator(App):
    CSS_PATH = "horizontal_layout.tcss"

    BINDINGS = [
        Binding("ctrl+s", "save", "Save", show=True) #todo: toast message
    ]

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.text = ""
        self.merge_tags = dict()
        
    def add_merge_tag(self, tag_name):
        if tag_name not in self.merge_tags:
            self.merge_tags[tag_name] = tag_name
    
    def cli(self, template_path): #Entry point from main.py
        self.parse_template(template_path)
        self.run()

    def parse_template(self, template_path):
        with open(template_path) as file:
            self.text = file.read()
        
        tags = re.findall(r"\{([^{}]+)\}", self.text) ##find anything between { and } except for { or } with at least 1 occurance to avoid empty tags and to only grab inner tags if nested
        for tag in tags:
            self.add_merge_tag(tag)

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(classes="box"): #box makes them take equal widths
                yield Static("Merge tags:\n")
                for tag_name, _ in self.merge_tags.items():
                    yield Static(tag_name)
                    # yield MergeTagInput(id=tag_name)
                    yield self.settings.create_input(tag_name)
                    yield Static("")
            
            yield Static(self.text, id="preview", classes="box")

    def update_merge_tag(self, tag_name, value):
        self.merge_tags[tag_name] = value
        self.update_preview(tag_name)

    def update_preview(self, current_tag=None):
        preview = self.query_one("#preview", Static)
        preview_text = self.replace_merge_tags(current_tag, True)
        preview.update(preview_text)
    
    #current_tag is the currently focused tag name that we want to highlight
    def replace_merge_tags(self, current_tag=None, recolor=False): #todo: parameter for colours
        replaced_text = self.text

        for tag_name in self.merge_tags:
            tag_value = self.merge_tags[tag_name]
            replacing_text = tag_value #This will be the value we replace {tag_name} with + any colours added

            if recolor:
                if current_tag is not None and tag_name == current_tag:
                    if tag_value != tag_name: #check if it's changed as it starts as tag_name: tag_name
                        replacing_text = addColor(replacing_text, "cyan") #todo: settings
                    else:
                        replacing_text = addColor(f"{{{replacing_text}}}", "cyan") #todo: settings
                elif tag_value != tag_name: #check if it's changed as it starts as tag_name: tag_name
                    replacing_text = addColor(replacing_text, "green") #todo: settings
                else:
                    replacing_text = addColor(f"{{{tag_value}}}", "red") #todo: settings
            
            replaced_text = replaced_text.replace(f"{{{tag_name}}}", replacing_text) #Replace all merge tags with the replacing_text
        return replaced_text

    def action_save(self):
        self.text = self.replace_merge_tags()
        with open("generated-readme.md", "w") as file:
            file.write(self.text)