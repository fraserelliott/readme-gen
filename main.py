import os
import sys
from readme_generator_textual import ReadmeGenerator
from settings import Settings
from PyInquirer import prompt

SETTINGS_PATH = "test-files/settings.json"
ROUTING_CHOICES = {
    "template_wizard": {
        "name": "Run template wizard",
        "value": "template_wizard"
    },
    "template_select": {
        "name": "Select template location to generate README",
        "value": "template_select"
    },
    "settings_wizard": {
        "name": "Run settings wizard",
        "value": "settings_wizard"
    },
    "quit": {
        "name": "Quit",
        "value": "quit"
    },
    "init_readme_generator": {
        "name": "Start README generator",
        "value": "init_readme_generator"
    }
}

class MainMenu:
    def __init__(self):
        self.settings = Settings()
        self.template_path = "test-files/template.md" #todo read from args
    
    def run(self):
        menu_choices = ("settings_wizard", "template_wizard", "init_readme_generator", "quit")
        self.select_menu("Select operation", menu_choices)

    def init_readme_generator(self):
        # Check whether it can load settings and attempt to load them as they're required by the generator

        # You need both a template and a settings file to be able to generate this, so first check each for existence. This will build an object to use for inquirer.select as it goes to not have to re-check. This will return anything it wants to run.

        data = dict()
        generator = ReadmeGenerator(self)

        if not os.path.exists(self.template_path):
            # Template doesn't exist so give some options.
            # todo: make these values in a const
            data["message"] = "Template {self.template_path} not found."
            data["choices"] = ["Run template wizard", "Give another template location", "Quit"]
            return data
        else:
            # Try parsing the template, if it fails then give some options
            if not generator.parse_template(self.template_path):
                data["message"] = "Template {self.template_path} failed to parse."
                data["choices"] = ["Run template wizard", "Give another template location", "Quit"]
        
        if not os.path.exists(SETTINGS_PATH):
            # settings file doesn't exist so give some options
            data["message"] = "Settings {SETTINGS_PATH} not found."
            data["choices"] = ["Run settings wizard", "Quit"]
            return data
        else:
            if not self.settings.load(SETTINGS_PATH):
                # settings file doesn't load so give some options
                data["message"] = "Settings {SETTINGS_PATH} failed to load."
                data["choices"] = ["Run settings wizard", "Quit"]
                return data
        
        # settings and template both successfully loaded so proceed to run the readme generator
        generator.settings = self.settings
        generator.run()
        self.run()        

    def select_menu(self, message:str, choices:tuple):
        menu_choices = [ROUTING_CHOICES[key] for key in choices]
        question = {
            "type": "list",
            "name":"action",
            "message": message,
            "choices": menu_choices
        }
        answers = prompt([question])
        getattr(self, answers["action"])()

    def template_select(self):
        question = { "type": "input", "name": "template_path", "message": "Enter the template file path" }        

    def quit(self):
        sys.exit(0)

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()