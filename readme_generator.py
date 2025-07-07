from rich.console import Console
from rich.layout import Layout
from rich import print
from merge_tag import MergeTag
import re

class ReadmeGenerator:
    def __init__(self, settings):
        self.settings = settings
        self.text = ""
        self.merge_tags = dict()

    def add_section(self, section):
        self.sections.append(section)
        
    def add_merge_tag(self, merge_tag):
        if merge_tag.tag_text not in self.merge_tags:
            self.merge_tags[merge_tag.tag_text] = merge_tag
    
    def cli(self, template_path):
        self.parse_template(template_path)
        console = Console()
        for tag in self.merge_tags.values():
            tag.prompt(console)
        self.replace_merge_tags()
        self.save()
            
    def parse_template(self, template_path):
        with open(template_path) as file:
            self.text = file.read()
        
        tags = re.findall(r"\{([^{}]+)\}", self.text) ##find anything between { and } except for { or } with at least 1 occurance to avoid empty tags and to only grab inner tags if nested
        for tag in tags:
            self.add_merge_tag(MergeTag(tag))
    
    def replace_merge_tags(self):
        for tag in self.merge_tags.values():
            self.text = self.text.replace(f"{{{tag.tag_text}}}", tag.value)
            
    def save(self):
        with open("generated-readme.md", "w") as file:
            file.write(self.text)
                
    def default(self): #test until I have the template reader made
        #Project title
        self.text = "# {project_title}"
        self.add_merge_tag(MergeTag("project_title"))