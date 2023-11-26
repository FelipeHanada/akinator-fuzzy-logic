import tkinter as tk
from random import shuffle
from functools import partial

from app.pages.page import Page
from app.components.footer import Footer
from app.components.genie_gif import GenieGIF

class QuestionsPage(Page):
    def __init__(self, container, controller):
        self.show_view = False
        
        super().__init__(container, controller, bg='#00100B')

    def setup(self):
        self.questions_stack = self.controller.responses_sheet_handler.get_questions()

        self.questions_stack = self.questions_stack[:3]
        shuffle(self.questions_stack)
        self.answered_questions_stack = []

        question = self.questions_stack[0]
        self.question_label['text'] = question

        if self.show_view:
            self.controller.fuzzynator.open_input_view(question)

        self.answers = {}

        self.selected_answer = None

    def select_answer(self, response: int):
        if self.questions_stack:
            if (self.selected_answer is not None):
                self.response_buttons[self.selected_answer]['state'] = tk.ACTIVE
            
            self.selected_answer = response
            self.next_question_button['state'] = tk.ACTIVE
            self.response_buttons[response]['state'] = tk.DISABLED

    def previous_question(self):
        if self.selected_answer:
            self.controller.result = self.controller.fuzzynator.compute_output(self.answers)
            
            self.response_buttons[self.selected_answer]['state'] = tk.ACTIVE
            self.selected_answer = None
        
        question = self.answered_questions_stack[0]
        self.answered_questions_stack.pop(0)
        del self.answers[question]
        self.questions_stack.insert(0, question)

        self.question_label['text'] = self.questions_stack[0]
        
        if not self.answered_questions_stack:
            self.previous_question_button['state'] = tk.DISABLED
        self.next_question_button['state'] = tk.ACTIVE

        self.selected_answer = None
    
    def next_question(self):
        if self.selected_answer is None:
            return
        
        question = self.questions_stack[0]
        self.questions_stack.pop(0)
        self.answered_questions_stack.append(question)
        self.answers[question] = self.selected_answer

        self.controller.result = self.controller.fuzzynator.compute_output(self.answers)

        if not self.questions_stack:
            self.controller.show_frame('guess_page')
            return
        
        self.question_label['text'] = self.questions_stack[0]
        
        self.response_buttons[self.selected_answer]['state'] = tk.ACTIVE
        self.previous_question_button['state'] = tk.ACTIVE
        self.next_question_button['state'] = tk.DISABLED
        self.selected_answer = None

    @staticmethod
    def output_minimum_difference(output):
        return output[0] - output[1]

    TITLE_FONT = ('Open Sans', 24)
    def create_header(self):
        self.header_frame = tk.Frame(self, bg=self['bg'])
        self.header_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.main_menu_button = tk.Button(
            self.header_frame,
            text='Menu',
            font=('Open Sans', 14),
            command=partial(self.controller.show_frame, 'main_menu')
        )
        self.main_menu_button.pack(side=tk.LEFT, padx=20, pady=5, fill=tk.BOTH)
        
        self.titulo = tk.Frame(self.header_frame, bg=self['bg'])
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

    QUESTION_FONT = ('Open Sans', 20)
    def create_question_frame(self):
        self.question_frame = tk.Frame(self, bg=self['bg'])
        self.question_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.genie_gif = GenieGIF(self.question_frame, bg=self['bg'])
        self.genie_gif.pack(side=tk.LEFT)

        self.question_label = tk.Label(
            self.question_frame,
            text='',
            font=('Open Sans', 20),
            wraplength=450,
            fg='white',
            justify=tk.CENTER,
            bg=self['bg']
        )
        self.question_label.pack(padx=20, pady=20, fill=tk.BOTH)

        self.buttons_frame = tk.Frame(self.question_frame, bg=self['bg'])
        self.response_buttons = []
        for v, ans in enumerate(('não', 'provavelmente não', 'talvez', 'provavelmente sim', 'sim')):
            button = tk.Button(
                self.buttons_frame,
                text=ans.capitalize(),
                font=('Open Sans', 12),
                command=partial(self.select_answer, v)
            )
            self.response_buttons.append(button)
            button.pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH)
        
        self.buttons_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        self.create_header()

        self.create_question_frame()

        self.questions_menu = tk.Frame(self, bg=self['bg'])
        self.questions_menu.pack()
        self.next_question_button = tk.Button(
            self.questions_menu,
            text='Próxima',
            font=('Open Sans', 14),
            command=self.next_question,
            state=tk.DISABLED
        )
        self.next_question_button.pack(side=tk.RIGHT, padx=20, pady=5, fill=tk.BOTH)

        self.previous_question_button = tk.Button(
            self.questions_menu,
            text='Voltar',
            font=('Open Sans', 14),
            command=self.previous_question,
            state=tk.DISABLED
        )
        self.previous_question_button.pack(side=tk.RIGHT, padx=20, pady=5, fill=tk.BOTH)

        self.footer = Footer(self, bg=self['bg'])
        self.footer.pack(side=tk.BOTTOM, pady=10)
