import argparse
import os
from readme_generator_textual import ReadmeGenerator
from settings import Settings

SETTINGS_LOCATION = "test-files/settings.json"
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
        # Check for whether it can load settings and attempt to load them as they're required by the generator
        
        # First look at whether we have a template and settings to be able to run the readme generator
        if os.path.exists(SETTINGS_LOCATION) and self.settings.load(SETTINGS_LOCATION):
            generator = ReadmeGenerator(self.settings)
            generator.cli(self.template_path)
        else:
            #Now we need to give options.
            pass

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()