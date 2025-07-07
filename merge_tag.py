from rich.console import Console
from PyInquirer import prompt as inquirer_prompt

#Default merge tag that requests a singular input based on the tag_text
class MergeTag:
    def __init__(self, tag_text):
        self.tag_text = tag_text
        self.value = tag_text

    def update_value(self, value):
        self.value = value

    def changed(self):
        return self.tag_text != self.value
    
    def equals(self, other):
        return self.tag_text == other.tag_text

    def prompt(self, console):
        #todo: get user input and store in self.value
        console.print(f"Please enter the value for [cyan]{{{self.tag_text}}}[/cyan]")
        question = {
            "type": "input",
            "name": "text",
            "message": "",
            "validate": lambda val: val != "" or "Value cannot be empty"
            }
        response = inquirer_prompt(question)
        self.value = response["text"]

#Requests a singular input from a set of options
class ListMergeTag(MergeTag):
    def __init__(self, tag_text, options):
        super().__init__(tag_text)
        self.options = options

    def prompt(self, console):
        #todo: get user input to select an option from the set self.options and store it in self.value
        pass

#Lets the user build a list with a set of prompts and continually asks if they want to add more. These are then converted into the text with a delimiter. e.g. for a contact section with options being {"email", "discord", "slack"} etc
class ListBuilderMergeTag(MergeTag):
    def __init__(self, tag_text, options, delimiter="\n"):
        super().__init__(tag_text)
        self.options = options
        self.delimiter = delimiter

    def prompt(self, console):
        inputs = []
        #todo: get user input, then concatenate with delimiter and store in self.value