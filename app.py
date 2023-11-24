import tkinter as tk

from responses_sheet_handler import ResponsesSheetHandler

from pages.main_menu import MainMenu
from pages.questions_page import QuestionsPage
from pages.guess_page import GuessPage

class App(tk.Tk):
    PAGES = {
        'main_menu': MainMenu,
        'questions_page': QuestionsPage,
        'guess_page': GuessPage
    }

    def __init__(self, responses_sheet_handler: ResponsesSheetHandler, fuzzynator: object):
        self.responses_sheet_handler = responses_sheet_handler
        self.fuzzynator = fuzzynator

        super().__init__()

        self.title('Fuzzynator')
        self.geometry('500x500')
        self.resizable(False, False)

        container = tk.Frame(self, bg='red')
        container.pack(fill="both", expand=True)
        
        self.active_page = None
        self.frames = {}
        for F in self.PAGES.values():
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.show_frame('main_menu')

    def show_frame(self, page_name: str):
        if self.active_page:
            self.frames[self.active_page].pack_forget()

        self.active_page = self.PAGES[page_name]
        
        self.frames[self.active_page].tkraise()
        self.frames[self.active_page].setup()

