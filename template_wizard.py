from PyInquirer import prompt
import prompt_utils
from string_utils import spaced_to_snake
from rich.console import Console
from typing import List

Y_N_VALIDATOR = "y_n"
GITHUB_CODE_LANGUAGES = ["actionscript3", "apache", "applescript", "asp", "bash", "brainfuck", "c", "cfm", "clojure", "cmake", "coffee", "coffeescript", "cpp", "cs", "csharp", "css", "csv", "diff", "elixir", "erb", "go", "groovy", "haml", "http", "java", "javascript", "json", "jsx", "less", "lolcode", "lua", "make", "markdown", "matlab", "nginx", "objectivec", "pascal", "perl", "php", "profile", "python", "r", "rb", "ruby", "rust", "salt", "saltstate", "scala", "scss", "shell", "sh", "zsh", "smalltalk", "sql", "svg", "swift", "ts", "typescript", "vim", "viml", "volt", "vhdl", "vue", "xml", "yaml"]

class TemplateWizard:
    def __init__(self, main_menu):
        self.main_menu = main_menu

    def run(self):
        question = prompt_utils.build_input("use_separator", "Add separator to each block?", Y_N_VALIDATOR)

        use_separator = prompt([question])["use_separator"]
        sections = [{
            "name": "Project Title",
            "type": "header", # this means it'll only have the header i.e. "# {project_title}"
            "header_level": "1" # this means it'll display #. 2 means ##, etc
        }]

        # Generate sections until the user doesn't want to add any more
        while True:
            question = prompt_utils.build_input("add_section", "Add new section?", Y_N_VALIDATOR)

            if prompt([question])["add_section"]:
                question1 = prompt_utils.build_input("name", "Section name: ")
                question2 = prompt_utils.build_list("header_level", "Header level: ", ["1", "2", "3"])
                question3 = prompt_utils.build_list("type", "Section type: ", ["Header", "Merge Tag", "Custom Text", "Code"])
                section = prompt([question1, question2, question3])

                if section["type"] == "code":
                    question = prompt_utils.build_list("language", "Code language: ", GITHUB_CODE_LANGUAGES)
                    section["language"] = prompt([question])["language"]
                elif section["type"] == "custom_text":
                    question = prompt_utils.build_input("custom_text", "Enter the text for this section, include any {{merge_tags}} you'd like: ")
                    section["text"] = prompt([question])["custom_text"]
                sections.append(section)
            else:
                break

        # Parse sections to create a readme template
        
        section_texts = []

        for section in sections:
            text = ""
            # Build Markdown header prefix based on header level (e.g. 1 -> '#', 2 -> '##')
            header_prefix = "#" * int(section["header_level"])
            section_title = section["name"]
            # section["name"] is raw user input so it needs to be changed for merge tags
            # anything created with a list is filtered with spaced_to_snake already so header_level, type and language don't need to be changed
            merge_tag = f"{{{spaced_to_snake(section_title)}}}"

            # build sections out depending on type
            if section["type"] == "header":
                text += f"{header_prefix} {merge_tag}\n"
            elif section["type"] == "merge_tag":
                text += f"{header_prefix} {section_title}\n"
                text += f"{merge_tag}\n"
            elif section["type"] == "custom_text":
                text += f"{header_prefix} {section_title}\n"
                text += f"{section['text']}\n"
            elif section["type"] == "code":
                text += f"{header_prefix} {section_title}\n"
                text += f"```{section['language']}\n"
                text += f"{merge_tag}\n"
                text += "```\n"
            section_texts.append(text)

        # add --- separator between sections if selected earlier
        if use_separator:
            text = "\n---\n".join(section_texts)
        else:
            text = "\n".join(section_texts)
        
        text = text.rstrip() # remove any trailing whitespace
        
        question = prompt_utils.build_input("template_path", "Path to save template: ")
        template_path = prompt([question])["template_path"]
        with open(template_path, "w") as file:
            file.write(text)
        
        console = Console()
        console.print(f"[green]Template saved to {template_path}[/green]")
        self.main_menu.template_path = template_path