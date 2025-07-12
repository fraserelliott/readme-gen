from merge_tag_inputs import MergeTagInput, MergeTagSelect
import json

INPUT_TYPE_REGISTRY = {
    "MergeTagInput": MergeTagInput,
    "MergeTagSelect": MergeTagSelect
}

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