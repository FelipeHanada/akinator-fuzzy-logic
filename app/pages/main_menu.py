import tkinter as tk
from app.pages.page import Page
from app.components.footer import Footer
from app.components.genie_gif import GenieGIF

from functools import partial

class MainMenu(Page):
    def __init__(self, container, controller):
        super().__init__(container, controller, bg='#00100B')

    TITLE_FONT = ('Open Sans', 36)
    def create_title(self):
        self.titulo = tk.Frame(self)
        self.titulo.pack()

        self.title_label1 = tk.Label(
            self.titulo,
            text='Fuzzy',
            font=self.TITLE_FONT,
            fg='white',
            bg=self['bg']
        )
        self.title_label1.pack(side=tk.LEFT, padx=0, pady=0)
        
        self.title_label2 = tk.Label(
            self.titulo,
            text='nator',
            font=self.TITLE_FONT,
            fg='#67AAE1',
            bg=self['bg']
        )
        self.title_label2.pack(side=tk.RIGHT, padx=0, pady=0)

    SUBTITLE_FONT = ('Open Sans', 14)
    def create_subtitle(self):
        self.subtitle = tk.Frame(self)
        self.subtitle.pack()

        self.subtitle_label = tk.Label(
            self.subtitle,
            text='O gênio que ',
            font=self.SUBTITLE_FONT,
            fg='white',
            bg=self['bg']
        )
        self.subtitle_label.pack(side=tk.LEFT, padx=0, pady=0)

        self.subtitle_label = tk.Label(
            self.subtitle,
            text='talvez ',
            font=self.SUBTITLE_FONT,
            fg='#67AAE1',
            bg=self['bg']
        )
        self.subtitle_label.pack(side=tk.LEFT, padx=0)

        self.subtitle_label = tk.Label(
            self.subtitle,
            text='saiba tudo...',
            font=self.SUBTITLE_FONT,
            fg='white',
            bg=self['bg']
        )
        self.subtitle_label.pack(side=tk.LEFT, padx=0)

    def create_widgets(self):
        self.create_title()
        self.create_subtitle()

        self.genie_gif = GenieGIF(self, bg=self['bg'])
        self.genie_gif.pack(pady=20)

        self.play_button = tk.Button(
            self,
            text='Jogar',
            font=('Open Sans', 16),
            width=8,
            command=partial(self.controller.show_frame, 'questions_page')
        )
        self.play_button.pack(padx=20)

        self.footer = Footer(self, bg=self['bg'])
        self.footer.pack(side=tk.BOTTOM, pady=10)
