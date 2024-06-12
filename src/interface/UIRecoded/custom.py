import tkinter

class ToggleButton(tkinter.Button):
    onSettings: dict
    offSettings: dict
    toggled: bool = False

    def __init__(self, settings: tuple, *args, **kwargs):
        self.onSettings, self.offSettings = settings

        super().__init__(*args, **kwargs)

    def toggle(self):
        if self.toggled:
            List = self.onSettings
        else:
            List = self.offSettings
        for setting in List:
            self[setting] = List[setting]
            
