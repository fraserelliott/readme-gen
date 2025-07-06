from rich.console import Console
from merge_tag import MergeTag

class ReadmeGenerator:
    def __init__(self, settings):
        self.settings = settings
        self.sections = list()
        self.header = ""

    def add_section(self, section):
        self.sections.append(section)
    
    def cli(self, template_path):
        console = Console()
        for section in self.sections:
            section.prompt(console)
            
    def parse_template(self, template_path):
        currentSection = None
        with open(template_path) as file:
            for line in file:
                if line[0] == "#":
                    section_title = line.lstrip("#").strip() #remove the starting # and any whitespace between to get the title
                    currentSection = Section(section_title, "") #Creating with "" as we add line later
                    self.add_section(currentSection)
            
                if currentSection:
                    currentSection.text += line
                else:
                    self.header += line #if we haven't started a section yet, then append to header
                    
        
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