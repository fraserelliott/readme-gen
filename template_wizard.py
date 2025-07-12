from PyInquirer import prompt
import prompt_utils

class TemplateWizard:
    def __init__(self, main_menu):
        self.main_menu = main_menu

    def run(self):
        names = ("Add separator to each block?")