from textual.widgets import Input

class MergeTagInput(Input):
    def __init__(self, id):
        super().__init__(id=id)
    
    def on_focus(self) -> None:
        self.app.update_preview(self.id)
    
    def on_blur(self) -> None:
        self.app.update_preview()

    def watch_value(self, value) -> None:
        self.app.update_merge_tag(self.id, value)