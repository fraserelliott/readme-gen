#Default merge tag that requests a singular input based on the tag_text
class MergeTag:
    def __init__(self, tag_text):
        self.tag_text = tag_text
        self.value = None

    def prompt(self):
        #todo: get user input and store in self.value
        pass

#Requests a singular input from a set of options
class ListMergeTag(MergeTag):
    def __init__(self, tag_text, options):
        super().__init__(tag_text)
        self.options = options

    def prompt(self):
        #todo: get user input to select an option from the set self.options and store it in self.value
        pass

#Lets the user build a list with a set of prompts and continually asks if they want to add more. These are then converted into the text with a delimiter. e.g. for a contact section with options being {"email", "discord", "slack"} etc
class ListBuilderMergeTag(MergeTag):
    def __init__(self, tag_text, options, delimiter="\n"):
        super().__init__(tag_text)
        self.options = options
        self.delimiter = delimiter

    def prompt(self):
        inputs = []
        #todo: get user input, then concatenate with delimiter and store in self.value