import os
import sys
from readme_generator_textual import ReadmeGenerator
from settings_wizard import SettingsWizard
from template_wizard import TemplateWizard
from settings import Settings
from PyInquirer import prompt

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
    SETTINGS_PATH = "test-files/settings.json"

    def __init__(self):
        self.settings = Settings()
        self.template_path = "test-files/template.md"
    
    def run(self):
        menu_choices = ("settings_wizard", "template_wizard", "init_readme_generator", "template_select", "quit")
        self.select_menu("Select operation", menu_choices)

    def init_readme_generator(self):
        # Check whether it can load settings and attempt to load them as they're required by the generator

        # You need both a template and a settings file to be able to generate this, so first check each for existence. This will build an object to use for inquirer.select as it goes to not have to re-check. This will return anything it wants to run.

        data = dict()
        generator = ReadmeGenerator(self)

        if not os.path.exists(self.template_path):
            # Template doesn't exist so give some options.
            # todo: make these values in a const
            data["message"] = f"Template {self.template_path} not found. Choose operation:"
            data["choices"] = ("template_wizard", "template_select", "quit")
            return data
        else:
            # Try parsing the template, if it fails then give some options
            if not generator.parse_template(self.template_path):
                data["message"] = f"Template {self.template_path} failed to parse. Choose operation:"
                data["choices"] = ("template_wizard", "template_select", "quit")
                return data
        
        if not os.path.exists(self.SETTINGS_PATH):
            # settings file doesn't exist so give some options
            data["message"] = f"Settings {self.SETTINGS_PATH} not found. Choose operation:"
            data["choices"] = ("settings_wizard", "quit")
            return data
        else:
            if not self.settings.load(self.SETTINGS_PATH):
                # settings file doesn't load so give some options
                data["message"] = f"Settings {self.SETTINGS_PATH} failed to load. Choose operation:"
                data["choices"] = ("settings_wizard", "quit")
                return data
        
        # settings and template both successfully loaded so proceed to run the readme generator
        generator.settings = self.settings
        generator.run()
        return None

    def select_menu(self, message:str, choices:tuple):
        menu_choices = [ROUTING_CHOICES[key] for key in choices]
        question = {
            "type": "list",
            "name":"action",
            "message": message,
            "choices": menu_choices
        }
        answers = prompt([question])
        res = getattr(self, answers["action"])()
        if res:
            self.select_menu(res["message"], res["choices"])

    def template_select(self):
        question = {
            "type": "input",
            "name": "template_path",
            "message": "Enter the template file path: ",
            "validate": lambda val: bool(val.strip()) or "Template path cannot be empty."
            }
        answers = prompt([question])
        self.template_path = answers["template_path"]
        res = self.init_readme_generator()
        if res:
            self.select_menu(res["message"], res["choices"])

    def template_wizard(self):
        wizard = TemplateWizard(self)
        wizard.run()
        return None
    
    def settings_wizard(self):
        wizard = SettingsWizard(self)
        wizard.run()
        return None

    def quit(self):
        sys.exit(0)

if __name__ == "__main__":
    menu = MainMenu()
    while True:
        menu.run()