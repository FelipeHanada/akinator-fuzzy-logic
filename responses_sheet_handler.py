import pandas as pd

class ResponsesSheetHandler:
    NAME_COLUMN = 'Insira o seu nome, com um sobrenome'

    def __init__(self):
        self.df = pd.read_excel('./data/data.xlsx')

    def get_questions(self):
        return [question for question in self.df.columns if question.startswith('Você')]
    
    def get_people(self):
        return self.df[self.NAME_COLUMN].tolist()
    
    def get_all_responses(self):
        return self.df[[self.NAME_COLUMN] + self.get_questions()]
    
    def get_response(self, person, question):
        return self.df[self.df[self.NAME_COLUMN] == person][question].values[0]
