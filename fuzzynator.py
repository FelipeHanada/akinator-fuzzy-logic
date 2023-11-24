import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from functools import reduce

from responses_sheet_handler import ResponsesSheetHandler

import matplotlib.pyplot as plt

class Fuzzynator(ctrl.ControlSystem):
    INPUT_NUMBER = 5
    INPUT_RANGE = 5
    INPUTS = ('no', 'probably no', 'maybe', 'probably yes', 'yes')
    OUTPUT_RANGE = 10
    OUTPUT_STEP = 1
    OUTPUTS = ('low', 'medium low', 'medium', 'medium high', 'high')

    def __init__(self, responses_sheet_handler: ResponsesSheetHandler, talkative: bool = False):
        self.responses_sheet_handler = responses_sheet_handler
        self.talkative = talkative

        self.input_variables = {}
        self.output_variables = {}

        super().__init__()

        self.create_input_variables()
        self.create_output_variables()
        self.create_rules()

        self.simulation = ctrl.ControlSystemSimulation(self)
        self.reset_responses()

    def create_input_variables(self):
        one_quarts = self.INPUT_RANGE / 4
        one_half = self.INPUT_RANGE / 2
        three_quarts = self.INPUT_RANGE * 3/4
        
        for question in self.responses_sheet_handler.get_questions():
            self.input_variables[question] = input = ctrl.Antecedent(np.arange(0, self.INPUT_RANGE + 1, self.INPUT_RANGE / self.INPUT_NUMBER), question)
            input[self.INPUTS[0]] = fuzz.trimf(self.input_variables[question].universe, [0, 0, three_quarts])
            input[self.INPUTS[1]] = fuzz.trimf(self.input_variables[question].universe, [0, one_quarts, three_quarts])
            input[self.INPUTS[2]] = fuzz.trimf(self.input_variables[question].universe, [0, one_half, self.INPUT_RANGE])
            input[self.INPUTS[3]] = fuzz.trimf(self.input_variables[question].universe, [one_quarts, three_quarts, self.INPUT_RANGE])
            input[self.INPUTS[4]] = fuzz.trimf(self.input_variables[question].universe, [one_quarts, self.INPUT_RANGE, self.INPUT_RANGE])
        
        if self.talkative:
            print("Input variables created")

    def create_output_variables(self):
        one_quarts = self.OUTPUT_RANGE / 4
        one_half = self.OUTPUT_RANGE / 2
        three_quarts = self.OUTPUT_RANGE * 3/4
    
        for person in self.responses_sheet_handler.get_people():
            self.output_variables[person] = ctrl.Consequent(np.arange(0, self.OUTPUT_RANGE + 1, self.OUTPUT_STEP), person)
            self.output_variables[person]['low'] = fuzz.trimf(self.output_variables[person].universe, [0, 0, three_quarts])
            self.output_variables[person]['medium low'] = fuzz.trimf(self.output_variables[person].universe, [0, one_quarts, three_quarts])
            self.output_variables[person]['medium'] = fuzz.trimf(self.output_variables[person].universe, [0, one_half, self.OUTPUT_RANGE])
            self.output_variables[person]['medium high'] = fuzz.trimf(self.output_variables[person].universe, [one_quarts, three_quarts, self.OUTPUT_RANGE])
            self.output_variables[person]['high'] = fuzz.trimf(self.output_variables[person].universe, [one_quarts, self.OUTPUT_RANGE, self.OUTPUT_RANGE])

        if self.talkative:
            print("Output variables created")

    def create_rules(self):
        responses = self.responses_sheet_handler.get_all_responses()

        for person in responses[self.responses_sheet_handler.NAME_COLUMN]:
            antecedents = { 'low': [], 'medium low': [], 'medium': [], 'medium high': [], 'high': [] }
            for question in self.responses_sheet_handler.get_questions():
                response = responses[question][responses[self.responses_sheet_handler.NAME_COLUMN] == person].iloc[0]

                for i, resp in enumerate(('no', 'probably no', 'maybe', 'probably yes', 'yes')):
                    r = int(response.lower() == 'sim')
                    antecedents[self.OUTPUTS[4 - abs(i - r * 4)]].append(self.input_variables[question][resp])
            
            for c, antecedent in antecedents.items():
                self.addrule(ctrl.Rule(reduce(lambda x, y: x & y, antecedent), self.output_variables[person][c]))
        
        if self.talkative:
            print("Rules created")

        """
        NO (0):
            "no" -> "high"
            "probably no" -> "medium high"
            "maybe" -> "medium"
            "probably yes" -> "medium low"
            "yes" -> "low"

        YES (1):
            "no" -> "low"
            "probably no" -> "medium low"
            "maybe" -> "medium"
            "probably yes" -> "medium high"
            "yes" -> "high"
        """

    def reset_responses(self):
        for question in self.responses_sheet_handler.get_questions():
            self.simulation.input[question] = (self.INPUT_NUMBER - 1) / 2
            # sets all the inputs to maybe
        
        if self.talkative:
            print("Responses reset")


    def set_response(self, question: str, response: int):
        self.simulation.input[question] = response

        if self.talkative:
            print(f"Response set: {question} = {response}")


    def open_input_view(self, question: str):
        self.input_variables[question].view(sim=self.simulation)

    
    def close_input_view(self, question):
        plt.close(question)
    
    def open_output_view(self, person: str):
        self.output_variables[person].view(sim=self.simulation)
    
    def close_output_view(self, person):
        plt.close(person)
    
    def close_views(self):
        plt.close('all')

    def compute_output(self):
        self.simulation.compute()

        if self.talkative:
            print("Output computed")
            print(self.simulation.output)

        # resultado = valor máximo
        # avaliar resultado com valor mínimo arbitrário L
        # e com diferença mínima H com o segundo maior valor

        return self.simulation.output
