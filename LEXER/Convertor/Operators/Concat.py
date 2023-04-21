from typing import List
from Convertor.Operators.Operator import Operator
from Automata.Automata import Automata
from Automata.EmptyToken import EmptyToken
from Convertor.Character import Character, character_types
from Convertor.Operators.Constants import CONCATENATION_SIMBOL, UNION_SIMBOL


class Concat(Operator):
    def __init__(self):
        super().__init__()
        self.simbol = CONCATENATION_SIMBOL
        self.priority = 2
        self.simbols = [self.kleene_simbol, self.simbol,
                        self.union_simbol, self.optional_simbol, self.plus_simbol]

    '''
		Validate the expression
		@param factors: list of factors
		@param index: index of the factor to validate
		@return: expression validated (str)
	'''

    def validate(self, factors: List[Character], index=0) -> List[Character]:
        final_exp = []
        keep_reading = True
        index = 0
        self_simbol = [
            Character(value=self.simbol, type=character_types.OPERATOR)]
        while keep_reading:
            if index >= len(factors):
                keep_reading = False
            # | not concat
            elif factors[index].value == self.union_simbol:
                final_exp += [factors[index]]
                index += 1
            # * concat if is not the last factor and the next factor is not a simbol or is not a agrupation close
            elif factors[index].value == self.kleene_simbol:
                final_exp += [factors[index]]
                if index < len(factors) - 1:
                    next_factor = factors[index + 1]
                    if next_factor.value not in self.simbols and next_factor.value != self.agrupation[1]:
                        final_exp += self_simbol
                index += 1
            # ? concat if is not the last factor and the next factor is not a simbol or is not a agrupation close
            elif factors[index].value == self.optional_simbol:
                final_exp += [factors[index]]
                if index < len(factors) - 1:
                    next_factor = factors[index + 1].value
                    if next_factor not in self.simbols and next_factor != self.agrupation[1]:
                        final_exp += self_simbol
                index += 1
            # + concat if is not the last factor and the next factor is not a simbol or is not a agrupation close
            elif factors[index].value == self.plus_simbol:
                final_exp += [factors[index]]
                if index < len(factors) - 1:
                    next_factor = factors[index + 1].value
                    if next_factor not in self.simbols and next_factor != self.agrupation[1]:
                        final_exp += self_simbol
                index += 1
            # ( not concat
            elif factors[index].value == self.agrupation[0]:
                final_exp += [factors[index]]
                index += 1
            # ) concat if is not the last factor and the next factor is not a simbol or is not a agrupation close
            elif factors[index].value == self.agrupation[1]:
                final_exp += [factors[index]]
                if index < len(factors) - 1:
                    next_factor = factors[index + 1].value
                    if next_factor not in self.simbols and next_factor != self.agrupation[1]:
                        final_exp += self_simbol
                index += 1
            # between two letters concat
            elif not self.is_simbol(factors[index].value):
                # final_exp += factors[index]
                # final_exp += factors[index + 1]
                # final_exp += factors[index + 2]
                # index += 3
                # if index < len(factors) - 1:
                # 	next_factor = factors[index]
                # 	if next_factor not in self.simbols and next_factor is not self.agrupation[1] and factors[index - 3:index] != str(ord('\\')).zfill(3):
                # 		final_exp += self.simbol
                final_exp += [factors[index]]
                if index < len(factors) - 1:
                    next_factor = factors[index + 1].value
                    if next_factor not in self.simbols and next_factor != self.agrupation[1]:
                        final_exp += self_simbol
                index += 1
        return final_exp

    def rules_concat(self, agrupation):
        expresion_concat = ''
        for index in range(len(agrupation)):
            caracter = agrupation[index]
            next_index = index + 1 if index < len(agrupation) - 1 else index
            if self.is_close_open_agrupation(caracter, agrupation[next_index]) or self.is_two_letters(caracter, agrupation[next_index]):
                expresion_concat += f'{caracter}{self.simbol if index < len(agrupation) - 1 else ""}'
            else:
                expresion_concat += caracter
        return expresion_concat

    def is_close_open_agrupation(self, caracter, next_caracter):
        return caracter is self.agrupation[1] and next_caracter is self.agrupation[0]

    def is_simbol(self, caracter):
        return caracter in self.simbols + self.agrupation

    def is_two_letters(self, caracter, next_caracter):
        return not self.is_simbol(caracter) and not self.is_simbol(next_caracter)

    def add_simbol_last_factor(self, factor, index):
        if index == len(factor) - 1:
            return ''
        next_caracter = factor[index + 1]
        if next_caracter is self.agrupation[1] and factor[index][-1] is self.agrupation[1]:
            return ''
        return self.simbol

    def get_automata_rule(self, operator1: Automata, operator2: Automata):
        # Remove the initial and final state of the operators
        operator1.final_state.is_final = False
        operator2.initial_state.is_initial = False
        # Remove first state of operator2
        missing_transitions = operator2.remove_state(operator2.initial_state)

        # Create temp automata
        automata = Automata()
        # New initial state
        automata.initial_state = operator1.initial_state
        # New final state
        automata.final_state = operator2.final_state
        # New transitions
        automata.transitions.transitions = operator1.transitions.transitions + \
            operator2.transitions.transitions
        for token, final_state in missing_transitions:
            automata.transitions.add_transition(
                operator1.final_state, token, final_state)
        # New States
        automata.states = operator1.states + operator2.states
        # New Alphabet
        automata.add_alphabet(operator1.alphabet + operator2.alphabet)
        return automata
