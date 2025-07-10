import argparse
import os
from readme_generator_textual import ReadmeGenerator
from settings import Settings

SETTINGS_PATH = "test-files/settings.json"

class MainMenu:
    def __init__(self):
        # Arg parsing and routing with options for -h or --help
        self.parser = argparse.ArgumentParser()
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument("--settings", action="store_true", help="Open settings configuration")
        group.add_argument("--template", action="store_true", help="Open template wizard")
        group.add_argument("--regenerate", action="store_true", help="Open regeneration wizard")

        self.settings = Settings()
        self.template_path = "test-files/template.md" #todo read from args
    
    def run(self):
        args = self.parser.parse_args()

        if args.settings:
            print("Not yet implemented.") #settings.cli()
        elif args.template:
            print("Not yet implemented.") #template_gen.cli()
        elif args.regenerate:
            print("Not yet implemented.") #readme_gen.regenerate()
        else:
            self.init_readme_generator()
    
    def init_readme_generator(self):
        # Check whether it can load settings and attempt to load them as they're required by the generator

        # You need both a template and a settings file to be able to generate this, so first check each for existence. This will build an object to use for inquirer.select as it goes to not have to re-check. This will return anything it wants to run.

        data = dict()
        generator = ReadmeGenerator()

        if not os.path.exists(self.template_path):
            # Template doesn't exist so give some options
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
        generator.cli()
        

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()