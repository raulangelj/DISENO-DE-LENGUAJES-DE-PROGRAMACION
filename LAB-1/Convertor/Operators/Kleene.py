from Convertor.Operators.Constants import KLEENE_SIMBOL, UNION_SIMBOL
from Convertor.Operators.Operator import Operator
from Automata.EmptyToken import EmptyToken
from Automata.Automata import Automata
from Automata.State import State


class Kleene(Operator):
    def __init__(self):
        super().__init__()
        self.simbol = KLEENE_SIMBOL
        self.priority = 3
        self.errors = [
            'Invalid expresion: kleene can\'t be the first simbol or follow a Union/Or operator\n',
        ]

    def validate(self, factors, index):  # sourcery skip: raise-specific-error
        # TODO: recorrer hacia adelante para ver si hay varios kleen juntos y quitarlos todos y dejar solo uno
        caracter_before = factors[-1] if len(factors) > 0 else ''
        if len(factors) == 0 or caracter_before is UNION_SIMBOL:
            # * can't be the first simbol
            raise Exception(self.errors[0])
        # [')',...]
        elif caracter_before == self.agrupation[1]:
            agrupation_kleen, positons_move = self.find_agrupation(factors)
            return f'{self.agrupation[0]}{agrupation_kleen}{self.simbol}{self.agrupation[1]}', positons_move
        # ['a|b', ...]
        elif len(caracter_before) > 1 and UNION_SIMBOL is caracter_before[-2]:
            letter = caracter_before[-1]
            return f'{caracter_before[:-1]}{self.agrupation[0]}{letter}{self.simbol}{self.agrupation[1]}', 1
        # ['(a*), ...]
        elif len(caracter_before) > 1 and caracter_before[-1] is self.agrupation[1]:
            group = caracter_before
            return f'{self.agrupation[0]}{group}{self.simbol}{self.agrupation[1]}', 1
        else:
            inside_parenthesis = len(caracter_before) > 1
            return f'{self.agrupation[0]}{self.agrupation[0] if inside_parenthesis else ""}{caracter_before}{self.agrupation[1] if inside_parenthesis else ""}{self.simbol}{self.agrupation[1]}', 1

    def get_automata_rule(self, automata_1:Automata) -> Automata:
        # New first state
        new_initial_state = State(is_initial=True)
        # New final state
        new_final_state = State(is_final=True)
        # New automata
        new_automata = Automata()
        # Change the initial state
        automata_1.initial_state.is_initial = False
        # Change the final state
        automata_1.final_state.is_final = False
        # Add the states
        new_automata.states =automata_1.states + [new_initial_state, new_final_state]
        # Add the alphabet
        new_automata.add_alphabet(automata_1.alphabet + [EmptyToken()])
        # Add the transitions
        new_automata.transitions = automata_1.transitions
        # Add the new transitions
        new_automata.transitions.add_transition(new_initial_state, EmptyToken(), automata_1.initial_state)
        new_automata.transitions.add_transition(new_initial_state, EmptyToken(), new_final_state)
        new_automata.transitions.add_transition(automata_1.final_state, EmptyToken(), automata_1.initial_state)
        new_automata.transitions.add_transition(automata_1.final_state, EmptyToken(), new_final_state)
        # Set the new initial and final states
        new_automata.initial_state = new_initial_state
        new_automata.final_state = new_final_state
        return new_automata
