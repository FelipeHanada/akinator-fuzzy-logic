import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from responses_sheet_handler import ResponsesSheetHandler

import matplotlib.pyplot as plt

cimport cython

class Fuzzynator(ctrl.ControlSystem):
    INPUT_RANGE = 5
    INPUTS = ('no', 'i dont know', 'yes')
    OUTPUT_RANGE = 100
    OUTPUTS = ('low', 'medium', 'high')

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

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def create_input_variables(self):
        one_quarts = self.INPUT_RANGE / 4
        one_half = self.INPUT_RANGE / 2
        three_quarts = self.INPUT_RANGE * 3/4
        
        for question in self.responses_sheet_handler.get_questions():
            input = ctrl.Antecedent(np.arange(0, self.INPUT_RANGE + 1, self.INPUT_RANGE / len(self.INPUTS)), question)
            
            input[self.INPUTS[0]] = fuzz.trimf(input.universe, [0, 0, three_quarts])
            input[self.INPUTS[1]] = fuzz.trimf(input.universe, [0, one_quarts, three_quarts])
            input[self.INPUTS[2]] = fuzz.trimf(input.universe, [0, one_half, self.INPUT_RANGE])
            input[self.INPUTS[3]] = fuzz.trimf(input.universe, [one_quarts, three_quarts, self.INPUT_RANGE])
            input[self.INPUTS[4]] = fuzz.trimf(input.universe, [one_quarts, self.INPUT_RANGE, self.INPUT_RANGE])
            
            self.input_variables[question] = input
        
        if self.talkative:
            print("Input variables created")

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def create_output_variables(self):
        one_quarts = self.OUTPUT_RANGE / 4
        one_half = self.OUTPUT_RANGE / 2
        three_quarts = self.OUTPUT_RANGE * 3/4
    
        for person in self.responses_sheet_handler.get_people():
            output = ctrl.Consequent(np.arange(0, self.OUTPUT_RANGE + 1, self.OUTPUT_STEP), person)
            
            output[self.OUTPUTS[0]] = fuzz.trimf(output.universe, [0, 0, three_quarts])
            output[self.OUTPUTS[1]] = fuzz.trimf(output.universe, [0, one_half, self.OUTPUT_RANGE])
            output[self.OUTPUTS[2]] = fuzz.trimf(output.universe, [one_quarts, self.OUTPUT_RANGE, self.OUTPUT_RANGE])
            
            self.output_variables[person] = output

        if self.talkative:
            print("Output variables created")

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def create_rules(self):
        pass

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

        return self.simulation.output
