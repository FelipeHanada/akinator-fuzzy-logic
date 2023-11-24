import tkinter as tk
from pages.page import Page

class MainMenu(Page):
    def __init__(self, container, controller):
        super().__init__(container, controller, bg='green')

    def create_widgets(self):
        self.title_label = tk.Label(self, text='Fuzzynator', font=('Arial', 24))
        self.title_label.pack(padx=20, pady=20, fill=tk.BOTH)

        self.play_button = tk.Button(
            self,
            text='Play',
            font=('Arial', 20),
            command=lambda: self.controller.show_frame('questions_page')
        )
        self.play_button.pack(padx=20, pady=20, fill=tk.BOTH)
