from merge_tag import MergeTag
import re
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input
from textual import events, on

class ReadmeGenerator(App):
    CSS_PATH = "horizontal_layout.tcss"

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.text = ""
        self.merge_tags = dict()
        
    def add_merge_tag(self, merge_tag):
        if merge_tag.tag_text not in self.merge_tags:
            self.merge_tags[merge_tag.tag_text] = merge_tag
    
    def cli(self, template_path):
        self.parse_template(template_path)
        self.run()

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(classes="box"):
                yield Static("Merge tags:")
                for tag_name, _ in self.merge_tags.items():
                    yield Static(tag_name)
                    yield Input(id=tag_name)
            
            yield Static(self.text, id="preview", classes="box")

    @on(Input.Changed)
    def update_tag(self, event: Input.Changed) -> None:
        assert event.input.id is not None
        tag_text = event.input.id
        current_value = event.input.value
        self.merge_tags[tag_text].update_value(current_value)
        self.update_preview()

    def update_preview(self):
        preview = self.query_one("#preview", Static)
        preview_text = self.replace_merge_tags()
        preview.update(preview_text)

            
    def parse_template(self, template_path):
        with open(template_path) as file:
            self.text = file.read()
        
        tags = re.findall(r"\{([^{}]+)\}", self.text) ##find anything between { and } except for { or } with at least 1 occurance to avoid empty tags and to only grab inner tags if nested
        for tag in tags:
            self.add_merge_tag(MergeTag(tag))
    
    def replace_merge_tags(self):
        replaced_text = self.text
        for tag in self.merge_tags.values():
            replaced_text = replaced_text.replace(f"{{{tag.tag_text}}}", tag.value)
        return replaced_text
            
    def save(self):
        self.text = self.replace_merge_tags()
        with open("generated-readme.md", "w") as file:
            file.write(self.text)
                
    def default(self): #test until I have the template reader made
        #Project title
        self.text = "# {project_title}"
        self.add_merge_tag(MergeTag("project_title"))