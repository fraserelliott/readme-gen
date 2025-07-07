from merge_tag_inputs import MergeTagInput, MergeTagSelect

INPUT_TYPE_REGISTRY = {
    "MergeTagInput": MergeTagInput,
    "MergeTagSelect": MergeTagSelect
}

class Settings:
    def __init__(self):
        self.tag_dict = dict()

    def add_tag(self, tag_name, config):
        self.tag_dict[tag_name] = config

    def create_input(self, tag_name):
        if tag_name not in self.tag_dict:
            return MergeTagInput(tag_name) # Default type for any merge tag

        configured_tag = self.tag_dict[tag_name]
        input_type = configured_tag.input_type
        input_class = INPUT_TYPE_REGISTRY[input_type]

        if not input_class:
            raise ValueError(f"Unknown input type: {input_type}")
        
        return input_class(tag_name, configured_tag.config)