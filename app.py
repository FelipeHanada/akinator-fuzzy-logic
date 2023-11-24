import tkinter as tk
from random import choice
from functools import partial

from responses_sheet_handler import ResponsesSheetHandler

class App(tk.Tk):
    def __init__(self, responses_sheet_handler: ResponsesSheetHandler, fuzzynator: object):
        self.responses_sheet_handler = responses_sheet_handler
        self.fuzzynator = fuzzynator
        self.show_view = False

        super().__init__()
        self.title('Fuzzynator')
        self.geometry('500x500')
        self.resizable(False, False)
        self.create_widgets()

        self.questions = self.responses_sheet_handler.get_questions()
        self.selected_answer = None
        self.get_question()


    def get_question(self):
        self.question = choice(self.questions)

        if not self.question:
            return
        
        self.questions.remove(self.question)
        self.question_label['text'] = self.question

        self.selected_answer = None
        self.next_question_button['state'] = tk.DISABLED
        
        if self.show_view:
            self.fuzzynator.close_views()
            self.fuzzynator.open_input_view(self.question)
    
    def answer_question(self, response: int):
        if self.question:
            self.fuzzynator.set_response(self.question, response)

            if (self.selected_answer is not None):
                self.response_buttons[self.selected_answer]['state'] = tk.ACTIVE
            
            self.selected_answer = response
            self.next_question_button['state'] = tk.ACTIVE
            self.response_buttons[response]['state'] = tk.DISABLED

    def next_question(self):
        if self.selected_answer is None:
            return

        if (self.selected_answer is not None):
            self.response_buttons[self.selected_answer]['state'] = tk.ACTIVE
        
        self.get_question()

    def create_widgets(self):
        self.question_label = tk.Label(self, text='', font=('Arial', 20), justify=tk.CENTER)
        self.question_label.pack(padx=20, pady=20, fill=tk.BOTH)

        self.views_frame = tk.Frame(self)
        self.views_frame.pack(padx=20, pady=20)

        self.buttons_frame = tk.Frame(self)
        self.response_buttons = []
        for v, ans in enumerate(('não', 'provavelmente não', 'talvez', 'provavelmente sim', 'sim')):
            button = tk.Button(
                self.buttons_frame,
                text=ans.capitalize(),
                font=('Arial', 16),
                command=partial(self.answer_question, v)
            )
            self.response_buttons.append(button)
            button.pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH)


        self.buttons_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.next_question_button = tk.Button(
            self,
            text='Próxima pergunta',
            font=('Arial', 16),
            command=self.next_question
        )
        self.next_question_button.pack(padx=20, pady=5, fill=tk.BOTH)

