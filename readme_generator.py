from rich.console import Console
from merge_tag import MergeTag

class ReadmeGenerator:
    def __init__(self, settings):
        self.settings = settings
        self.sections = list()

    def add_section(self, section):
        self.sections.append(section)
    
    def cli(self, template_path):
        console = Console()
        for section in self.sections:
            section.prompt(console)
        
    def default(self): #test until I have the template reader made
        #Project title
        project_title = Section("Project Title", "# {project_title}")
        project_title.add_merge_tag(MergeTag("project_title"))
        self.add_section(project_title)

class Section:
    def __init__(self, section_name, text):
        self.section_name = section_name
        self.text = text
        self.merge_tags = list()
    
    def add_merge_tag(self, merge_tag):
        self.merge_tags.append(merge_tag)
    
    def prompt(self, console):
        console.print(f"[bold green]Starting section {self.section_name}[/bold green]")
        for tag in self.merge_tags:
            tag.prompt(console)