import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.defuzzify import defuzz

from functools import reduce
from math import floor

from responses_sheet_handler import ResponsesSheetHandler


class Fuzzynator:
    def __init__(self, responses_sheet_handler: ResponsesSheetHandler, talkative: bool = False):
        self.responses_sheet_handler = responses_sheet_handler
        self.talkative = talkative

        self.input_variables = {}
        self.output_variables = {}
        self.rules = []

        self.create_input_variables()
        self.create_output_variables()
        self.create_rules()
        
        if self.talkative:
            print("Fuzzynator created")

    INPUT_RANGE = 5
    INPUTS = ('no', 'probably no', 'i dont know', 'probably yes', 'yes')
    INPUT_UNIVERSE = np.arange(0, INPUT_RANGE + 1, INPUT_RANGE / len(INPUTS))
    def create_input_variables(self):
        one_quarts = self.INPUT_RANGE / 4
        one_half = self.INPUT_RANGE / 2
        three_quarts = self.INPUT_RANGE * 3/4
        
        for question in self.responses_sheet_handler.get_questions():
            input = ctrl.Antecedent(self.INPUT_UNIVERSE, question)
            
            input[self.INPUTS[0]] = fuzz.trimf(input.universe, [0, 0, one_half])
            input[self.INPUTS[1]] = fuzz.trimf(input.universe, [0, one_quarts, self.INPUT_RANGE])
            input[self.INPUTS[2]] = fuzz.trimf(input.universe, [0, one_half, self.INPUT_RANGE])
            input[self.INPUTS[3]] = fuzz.trimf(input.universe, [0, three_quarts, self.INPUT_RANGE])
            input[self.INPUTS[4]] = fuzz.trimf(input.universe, [one_half, self.INPUT_RANGE, self.INPUT_RANGE])
            
            self.input_variables[question] = input

        if self.talkative:
            print("Input variables created")

    OUTPUT_RANGE = 100
    OUTPUTS = ('low', 'medium low', 'medium', 'medium high', 'high')
    OUTPUT_UNIVERSE = np.arange(0, OUTPUT_RANGE + 1, 0.1)
    def create_output_variables(self):
        one_quarts = self.OUTPUT_RANGE / 4
        one_half = self.OUTPUT_RANGE / 2
        three_quarts = self.OUTPUT_RANGE * 3/4
    
        for person in self.responses_sheet_handler.get_people():
            output = ctrl.Consequent(self.OUTPUT_UNIVERSE, person)
            
            output[self.OUTPUTS[0]] = fuzz.trimf(output.universe, [0, 0, three_quarts])
            output[self.OUTPUTS[1]] = fuzz.trimf(output.universe, [0, one_quarts, self.OUTPUT_RANGE])
            output[self.OUTPUTS[2]] = fuzz.trimf(output.universe, [0, one_half, self.OUTPUT_RANGE])
            output[self.OUTPUTS[3]] = fuzz.trimf(output.universe, [0, three_quarts, self.OUTPUT_RANGE])
            output[self.OUTPUTS[4]] = fuzz.trimf(output.universe, [one_quarts, self.OUTPUT_RANGE, self.OUTPUT_RANGE])
            
            self.output_variables[person] = output

        if self.talkative:
            print("Output variables created")

    def create_rules(self):
        for person in self.responses_sheet_handler.get_people():
            for output_i, output_mf in enumerate(self.OUTPUTS):
                antecedents = []

                for question in self.responses_sheet_handler.get_questions():
                    response = self.responses_sheet_handler.get_response(person, question)
                    response_value = int(response == 'sim')
                    input_mf = self.INPUTS[len(self.INPUTS) - 1 - abs(output_i - response_value * (len(self.INPUTS) - 1))]
                    antecedent = self.input_variables[question][input_mf]
                    antecedents.append(antecedent)

                rule = {'antecedents': antecedents, 'consequent': self.output_variables[person][output_mf]}
                self.rules.append(rule)

        if self.talkative:
            print(f"{len(list(self.rules))} rules created")

    def compute_firing_strength(self):
        pass
    
    def compute_consequences(self):
        pass

    def compute_output(self, input_values: dict)->dict:
        for question in self.responses_sheet_handler.get_questions():
            if question not in input_values:
                input_values[question] = floor(self.INPUT_RANGE / 2)

        firing_strengths = self.compute_firing_strength()
        consequences = self.compute_consequences()