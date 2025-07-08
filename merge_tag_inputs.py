from textual.widgets import Input, Select

class MergeTagInput(Input):
    def __init__(self, id, config = None):
        super().__init__(id=id)
    
    def on_focus(self) -> None:
        self.app.update_preview(self.id)
    
    def on_blur(self) -> None:
        self.app.update_preview()

    def watch_value(self, value) -> None:
        self.app.update_merge_tag(self.id, value)

class MergeTagSelect(Select):
    def __init__(self, id, config = None):
        super().__init__(id=id, options=[(item, item) for item in config["options"]])

    def on_focus(self) -> None:
        self.app.update_preview(self.id)
    
    def on_blur(self) -> None:
        self.app.update_preview()

    def watch_value(self, value) -> None:
        if value == Select.BLANK:
            self.app.update_merge_tag(self.id, self.id)
        else:
            self.app.update_merge_tag(self.id, value)