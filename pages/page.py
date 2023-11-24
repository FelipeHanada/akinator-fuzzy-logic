import tkinter as tk

class Page(tk.Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.controller = controller
        self.create_widgets()

        self.setup()

    def setup(self):
        pass

    def create_widgets(self):
        pass
