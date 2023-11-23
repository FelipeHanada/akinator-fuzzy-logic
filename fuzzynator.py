import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from infra.repository.question_repository import QuestionRepository
from infra.repository.person_repository import PersonRepository
from infra.repository.response_repository import ResponseRepository

class Fuzzynator:
    def __init__(self):
        self.input_variables = {}
        self.output_variables = {}
        self.rules = []
        self.question_repository = QuestionRepository()
        self.person_repository = PersonRepository()
        self.response_repository = ResponseRepository()

    INPUT_NUMBER = 5
    INPUT_RANGE = 5
    def create_input_variables(self):
        one_quarts = self.INPUT_RANGE / 4
        one_half = self.INPUT_RANGE / 2
        three_quarts = self.INPUT_RANGE * 3/4
        
        for question in self.question_repository.select_all():
            self.input_variables[question.id] = ctrl.Antecedent(np.arange(0, self.INPUT_RANGE + 1, self.INPUT_RANGE / self.INPUT_NUMBER), question.text)
            self.input_variables[question.id]['no'] = fuzz.trimf(self.input_variables[question.id].universe, [0, 0, three_quarts])
            self.input_variables[question.id]['probably no'] = fuzz.trimf(self.input_variables[question.id].universe, [0, one_quarts, three_quarts])
            self.input_variables[question.id]['maybe'] = fuzz.trimf(self.input_variables[question.id].universe, [0, one_half, self.INPUT_RANGE])
            self.input_variables[question.id]['probably yes'] = fuzz.trimf(self.input_variables[question.id].universe, [one_quarts, three_quarts, self.INPUT_RANGE])
            self.input_variables[question.id]['yes'] = fuzz.trimf(self.input_variables[question.id].universe, [one_quarts, self.INPUT_RANGE, self.INPUT_RANGE])

    OUTPUT_RANGE = 10
    OUTPUT_STEP = 1
    def create_output_variables(self):
        one_quarts = self.OUTPUT_RANGE / 4
        one_half = self.OUTPUT_RANGE / 2
        three_quarts = self.OUTPUT_RANGE * 3/4
    
        for person in self.person_repository.select_all():
            self.output_variables[person.id] = ctrl.Consequent(np.arange(0, self.OUTPUT_RANGE + 1, self.OUTPUT_STEP), person.name)
            self.output_variables[person.id]['low'] = fuzz.trimf(self.output_variables[person.id].universe, [0, 0, three_quarts])
            self.output_variables[person.id]['medium low'] = fuzz.trimf(self.output_variables[person.id].universe, [0, one_quarts, three_quarts])
            self.output_variables[person.id]['medium'] = fuzz.trimf(self.output_variables[person.id].universe, [0, one_half, self.OUTPUT_RANGE])
            self.output_variables[person.id]['medium high'] = fuzz.trimf(self.output_variables[person.id].universe, [one_quarts, three_quarts, self.OUTPUT_RANGE])
            self.output_variables[person.id]['high'] = fuzz.trimf(self.output_variables[person.id].universe, [one_quarts, self.OUTPUT_RANGE, self.OUTPUT_RANGE])

    def create_rules(self):
        for response in self.response_repository.select_all():

            outputs = ('low', 'medium low', 'medium', 'medium high', 'high')
            for i, resp in enumerate(('no', 'probably no', 'maybe', 'probably yes', 'yes')):
                antecedent = self.input_variables[response.question_id][resp]
                consequent = self.output_variables[response.person_id][outputs[4 - abs(i - response.response * 4)]]

                self.rules.append(ctrl.Rule(antecedent, consequent))

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

    def compute_output(self):
        fuzzy_system = ctrl.ControlSystem(self.rules)
        simulation = ctrl.ControlSystemSimulation(fuzzy_system)

        for question in self.question_repository.select_all():
            simulation.input[question.id] = (self.INPUT_NUMBER - 1) / 2
            # sets all the inputs to maybe

        # we need to input the questions here

        simulation.compute()
        output_value = simulation.output['output_variable']
        return output_value
