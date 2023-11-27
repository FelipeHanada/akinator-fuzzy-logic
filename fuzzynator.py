import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from responses_sheet_handler import ResponsesSheetHandler

import matplotlib.pyplot as plt

from functools import reduce
from math import floor

import numpy as np

class Fuzzynator(ctrl.ControlSystem):
    INPUT_RANGE = 5
    INPUTS = ('no', 'probably no', 'i dont know', 'probably yes', 'yes')
    OUTPUT_RANGE = 100
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

        if self.talkative:
            print("Fuzzynator created")

    def create_input_variables(self):
        one_quarts = self.INPUT_RANGE / 4
        one_half = self.INPUT_RANGE / 2
        three_quarts = self.INPUT_RANGE * 3/4
        
        for question in self.responses_sheet_handler.get_questions():
            input = ctrl.Antecedent(np.arange(0, self.INPUT_RANGE + 1, self.INPUT_RANGE / len(self.INPUTS)), question)
            
            input[self.INPUTS[0]] = fuzz.trimf(input.universe, [0, 0, one_half])
            input[self.INPUTS[1]] = fuzz.trimf(input.universe, [0, one_quarts, self.INPUT_RANGE])
            input[self.INPUTS[2]] = fuzz.trimf(input.universe, [0, one_half, self.INPUT_RANGE])
            input[self.INPUTS[3]] = fuzz.trimf(input.universe, [0, three_quarts, self.INPUT_RANGE])
            input[self.INPUTS[4]] = fuzz.trimf(input.universe, [one_half, self.INPUT_RANGE, self.INPUT_RANGE])
            
            self.input_variables[question] = input

        if self.talkative:
            print("Input variables created")

    def create_output_variables(self):
        one_quarts = self.OUTPUT_RANGE / 4
        one_half = self.OUTPUT_RANGE / 2
        three_quarts = self.OUTPUT_RANGE * 3/4
    
        for person in self.responses_sheet_handler.get_people():
            output = ctrl.Consequent(np.arange(0, self.OUTPUT_RANGE + 1, 0.1), person)
            
            output[self.OUTPUTS[0]] = fuzz.trimf(output.universe, [0, 0, three_quarts])
            output[self.OUTPUTS[1]] = fuzz.trimf(output.universe, [0, one_quarts, self.OUTPUT_RANGE])
            output[self.OUTPUTS[2]] = fuzz.trimf(output.universe, [0, one_half, self.OUTPUT_RANGE])
            output[self.OUTPUTS[3]] = fuzz.trimf(output.universe, [0, three_quarts, self.OUTPUT_RANGE])
            output[self.OUTPUTS[4]] = fuzz.trimf(output.universe, [one_quarts, self.OUTPUT_RANGE, self.OUTPUT_RANGE])
            
            self.output_variables[person] = output

        if self.talkative:
            print("Output variables created")

    def create_rules_old(self):
        for person in self.responses_sheet_handler.get_people():
            for output_i, output_mf in enumerate(self.OUTPUTS):
                antecedents = []

                for question in self.responses_sheet_handler.get_questions():
                    response = self.responses_sheet_handler.get_response(person, question)
                    response_value = int(response == 'sim')
                    input_mf = self.INPUTS[len(self.INPUTS) - 1 - abs(output_i - response_value * (len(self.INPUTS) - 1))]
                    antecedent = self.input_variables[question][input_mf]
                    antecedents.append(antecedent)

                rule = ctrl.Rule(reduce(lambda x, y: x & y, antecedents), self.output_variables[person][output_mf])
                self.addrule(rule)

    def create_rules(self):
        for person in self.responses_sheet_handler.get_people():
            for output_i, output_mf in enumerate(self.OUTPUTS):
                for question in self.responses_sheet_handler.get_questions():
                    response = self.responses_sheet_handler.get_response(person, question)
                    response_value = int(response.lower() == 'sim')
                    input_mf = self.INPUTS[len(self.INPUTS) - 1 - abs(response_value * (len(self.INPUTS) - 1) - output_i)]

                    antecedent = self.input_variables[question][input_mf]
                    consequent = self.output_variables[person][output_mf]

                    rule = ctrl.Rule(antecedent, consequent)
                    print(rule)
                    self.addrule(rule)

        """
        response = yes
        no -> low
        probably no -> medium low
        i dont know -> medium
        probably yes -> medium high
        yes -> high

        response = no
        no -> high
        probably no -> medium high
        i dont know -> medium
        probably yes -> medium low
        yes -> low
        """

        if self.talkative:
            print(f"{len(list(self.rules))} rules created")

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

    def compute_output(self, answers: dict):
        for question in self.responses_sheet_handler.get_questions():
            self.simulation.input[question] = floor((len(self.INPUTS) - 1) / 2)
        
        print(answers)
        for question, answer in answers.items():
            self.simulation.input[question] = answer

        self.simulation.compute()

        if self.talkative:
            print("Output computed")
            print(self.simulation.output)

        return self.simulation.output
