from Automata.Automata import Automata
from termcolor import colored

class DFA(Automata):
    def __init__(self):
        super().__init__()

    def simulate(self, input_string: str) -> str:
        current_state = self.initial_state
        for caracter in input_string:
            current_state = self.move(current_state, caracter)
        is_valid = current_state.is_final
        if is_valid:
            return colored(f'"{input_string}" is valid', 'green')
        else:
            return colored(f'"{input_string}" is invalid', 'red')
        