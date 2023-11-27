import tkinter as tk
from functools import partial

from app.pages.page import Page

from app.components.genie_gif import GenieGIF
from app.components.footer import Footer

from random import choice

class GuessPage(Page):
    def __init__(self, container, controller):
        super().__init__(container, controller, bg='#00100B')

    def setup(self):
        result = next(iter(self.controller.result.items()))
        self.name_label['text'] = choice(self.controller.responses_sheet_handler.get_people())

    TITLE_FONT = ('Open Sans', 24)
    def create_header(self):
        self.titulo = tk.Frame(self, bg=self['bg'])
        self.titulo.pack()

        self.title_label1 = tk.Label(
            self.titulo,
            text='Fuzzy',
            font=self.TITLE_FONT,
            fg='white',
            bg=self['bg']
        )
        self.title_label1.pack(side=tk.LEFT, padx=0)
        
        self.title_label2 = tk.Label(
            self.titulo,
            text='nator',
            font=self.TITLE_FONT,
            fg='#67AAE1',
            bg=self['bg']
        )
        self.title_label2.pack(side=tk.RIGHT, padx=0)

    def create_widgets(self):
        self.create_header()

        self.main_wrapper = tk.Frame(self, bg=self['bg'])
        self.main_wrapper.pack(pady=50)

        self.genie_gif = GenieGIF(self.main_wrapper, bg=self['bg'])
        self.genie_gif.pack(side=tk.LEFT)

        self.guess_frame = tk.Frame(self.main_wrapper, bg=self['bg'])
        self.guess_frame.pack(side=tk.RIGHT)

        self.hum_label = tk.Label(
            self.guess_frame,
            text='Hummmmm...',
            font=('Open Sans', 20),
            fg='white',
            justify=tk.CENTER,
            bg=self['bg']
        )
        self.hum_label.pack()

        self.guess_label = tk.Label(
            self.guess_frame,
            text='Você é',
            font=('Open Sans', 20),
            fg='white',
            justify=tk.CENTER,
            bg=self['bg']
        )
        self.guess_label.pack()

        self.name_label = tk.Label(
            self.guess_frame,
            text='',
            font=('Open Sans', 20),
            fg='#67AAE1',
            justify=tk.CENTER,
            bg=self['bg']
        )
        self.name_label.pack()

        self.play_again_button = tk.Button(
            self,
            text='Jogar novamente',
            font=('Open Sans', 16),
            command=partial(self.controller.show_frame, 'main_menu')
        )
        self.play_again_button.pack()

        self.footer = Footer(self, bg=self['bg'])
        self.footer.pack(side=tk.BOTTOM, pady=10)

