from rich.console import Console

class ReadmeGenerator:
    def __init__(self, settings):
        self.settings = settings
        self.sections = dict()

    def cli(self, template_path):
        console = Console()

class Section:
    def __init__(self, section_name, text):
        self.section_name = section_name
        self.text = text
        self.merge_tags = list()
    
    def add_merge_tag(self, merge_tag):
        self.merge_tags.append(merge_tag)