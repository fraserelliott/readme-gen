from merge_tag_inputs import MergeTagInput, MergeTagSelect
from PyInquirer import prompt
import prompt_utils
from string_utils import spaced_to_snake
from rich.console import Console
import json

INPUT_TYPE_REGISTRY = {
    "MergeTagInput": MergeTagInput,
    "MergeTagSelect": MergeTagSelect
}

Y_N_VALIDATOR = "y_n"

class Settings:
    def __init__(self):
        self.tag_dict = dict()

    def load(self, file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                for tag in data:
                    tag_name = tag["tag_name"]
                    config = tag["config"]
                    self.add_tag(tag_name, config)
            return True
        except Exception as e:
            print("An error occured: ", e)
            self.tag_dict = dict() #return it to an empty dict as loading failed
            return False
            

    def add_tag(self, tag_name, config):
        # print(f"Adding tag {tag_name} with config {config}")
        self.tag_dict[tag_name] = config

    def create_input(self, tag_name):
        if tag_name not in self.tag_dict:
            return MergeTagInput(tag_name) # Default type for any merge tag

        configured_tag = self.tag_dict[tag_name]
        input_type = configured_tag["input_type"]
        input_class = INPUT_TYPE_REGISTRY[input_type]

        if not input_class:
            raise ValueError(f"Unknown input type: {input_type}")
        
        return input_class(tag_name, configured_tag)


class SettingsWizard:
    def __init__(self, main_menu):
        self.main_menu = main_menu
    
    def run(self):
        tags = []

        while True:
            question = prompt_utils.build_input("add_tag", "Configure new tag to be a list with set options?", Y_N_VALIDATOR)
            if not prompt([question])["add_tag"]:
                break

            # Build initial tag object
            question = prompt_utils.build_input("tag_name", "Tag name: ")
            tag = { "tag_name": prompt([question])["tag_name"]  }
            tag["config"] = { "input_type": "MergeTagSelect", "options": []}

            # Add options to tag object
            while True:
                question = prompt_utils.build_input("add_option", f"Add new option to list for {tag['tag_name']}?", Y_N_VALIDATOR)
                if not prompt([question])["add_option"]:
                    break

                question = prompt_utils.build_input("tag_option", "Enter option: ")
                tag["config"]["options"].append(prompt([question])["tag_option"])
            
            tags.append(tag)

        if not tags:
            console = Console()
            console.print("[red]No tags were configured.[/red]")
            question = prompt_utils.build_input("save_blank", "Do you want to save a blank settings file?", Y_N_VALIDATOR)

            if not prompt([question])["save_blank"]:
                return
        
        # Save settings to default path
        with open(self.main_menu.SETTINGS_PATH, "w") as file:
            json.dump(tags, file, indent=2)

        # Load settings straight away
        self.main_menu.settings.load(self.main_menu.SETTINGS_PATH)