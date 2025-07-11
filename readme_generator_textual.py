from merge_tag_inputs import MergeTagInput
import re
import sys
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.binding import Binding
from textual.widgets import Static

#usage: addColor("foo", "red") => "[red]foo[/red]"
def addColor(str, color):
    return f"[{color}]{str}[/{color}]"

class ReadmeGenerator(App):
    CSS_PATH = "layout.tcss"

    BINDINGS = [
        Binding("ctrl+s", "save", "Save", show=True, priority=True),
        Binding("ctrl+x", "terminate", "terminate", show=True, priority=True)
    ]

    DEFAULT_MESSAGE = "Ctrl+X to quit | Ctrl+S to save | Ctrl+Q to return to main menu"

    def __init__(self, main_menu, settings=None):
        super().__init__()
        self.settings = settings
        self.main_menu = main_menu
        self.text = ""
        self.merge_tags = dict()
        
    def add_merge_tag(self, tag_name):
        if tag_name not in self.merge_tags:
            self.merge_tags[tag_name] = tag_name

    def parse_template(self, template_path):
        with open(template_path, encoding="utf-8") as file:
            self.text = file.read()
        
        tags = re.findall(r"\{([^{}]+)\}", self.text) # find anything between { and } except for { or } with at least 1 occurance to avoid empty tags and to only grab inner tags if nested
        if not tags:
            return False

        for tag in tags:
            self.add_merge_tag(tag)
        
        return True

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                with Vertical(classes="box"): #box makes them take equal widths
                    yield Static("Merge tags:\n")
                    for tag_name, _ in self.merge_tags.items():
                        yield Static(tag_name)
                        yield self.settings.create_input(tag_name)
                        yield Static()
                
                with Container(classes="box"):
                    yield Static(self.text, id="preview")
        
            self.statusbar = Static(self.DEFAULT_MESSAGE, id="statusbar")
            yield self.statusbar

    def update_merge_tag(self, tag_name, value):
        self.merge_tags[tag_name] = value
        self.update_preview(tag_name)

    def update_preview(self, current_tag=None):
        preview = self.query_one("#preview", Static)
        preview_text = self.replace_merge_tags(current_tag, True)
        preview.update(preview_text)
    
    #current_tag is the currently focused tag name that we want to highlight
    def replace_merge_tags(self, current_tag=None, recolor=False):
        replaced_text = self.text

        for tag_name in self.merge_tags:
            tag_value = self.merge_tags[tag_name]
            replacing_text = tag_value #This will be the value we replace {tag_name} with + any colours added

            if recolor:
                if current_tag is not None and tag_name == current_tag:
                    if tag_value != tag_name: #check if it's changed as it starts as tag_name: tag_name
                        replacing_text = addColor(replacing_text, "cyan")
                    else:
                        replacing_text = addColor(f"{{{replacing_text}}}", "cyan") # wrap in { } as the text hasn't changed yet so merge_tag should be {merge_tag} in the preview
                elif tag_value != tag_name: #check if it's changed as it starts as tag_name: tag_name
                    replacing_text = addColor(replacing_text, "green")
                else:
                    replacing_text = addColor(f"{{{tag_value}}}", "red")
            
            replaced_text = replaced_text.replace(f"{{{tag_name}}}", replacing_text) #Replace all merge tags with the replacing_text
        return replaced_text

    def action_save(self):
        self.text = self.replace_merge_tags()
        with open("generated-readme.md", "w") as file:
            file.write(self.text)
        
        self.statusbar.update("Saved generated-readme.md!")
        self.set_timer(2, lambda: self.statusbar.update(self.DEFAULT_MESSAGE))

    def action_terminate(self):
        sys.exit(0)