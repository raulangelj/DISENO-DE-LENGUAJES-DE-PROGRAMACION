from Convertor.Operators.Constants import OPEN_AGRUPATION_SIMBOL, CLOSE_AGRUPATION_SIMBOL, EMPTY_SIMBOL, CONCATENATION_SIMBOL, KLEENE_SIMBOL, UNION_SIMBOL, OPTIONAL_SIMBOL, PLUS_SIMBOL
from Convertor.Character import *
from typing import List, Tuple


class Operator():
    def __init__(self):
        self.simbol = ''
        self.priority = -1
        self.empty_simbol = EMPTY_SIMBOL
        self.concatenation_simbol = CONCATENATION_SIMBOL
        self.kleene_simbol = KLEENE_SIMBOL
        self.union_simbol = UNION_SIMBOL
        self.optional_simbol = OPTIONAL_SIMBOL
        self.plus_simbol = PLUS_SIMBOL
        self.agrupation = [OPEN_AGRUPATION_SIMBOL, CLOSE_AGRUPATION_SIMBOL]

    def get_simbol(self):
        return self.simbol

    def get_priority(self):
        return self.priority

    def validate(self, expresion, index):
        return expresion

    def get_agrupation_simbols(self):
        return self.agrupation

    '''
		* Find the agrupation of the expresion
		@param expresion: the expresion to find the agrupation
		@param forward: if the agrupation is forward or backward
		@return: the agrupation expresion and the number of positions to move
	'''

    def find_agrupation(self, expresion: List[Character]) -> Tuple[List[Character], int]:
        close_agrupation_count = 0
        start_expresion = False
        agrupation_exp = []
        positions_move = 0
        for i in range(len(expresion) - 1, -1, -1):
            caracter = expresion[i]
            if caracter.value == self.agrupation[1]:
                start_expresion = True
                close_agrupation_count += 1
            if start_expresion:
                agrupation_exp.insert(0, caracter)
            if caracter.value == self.agrupation[0] and close_agrupation_count > 0:
                close_agrupation_count -= 1
                start_expresion = close_agrupation_count > 0
            if close_agrupation_count == 0:
                positions_move += 1
                break
            positions_move += 1
        return agrupation_exp, positions_move

    def find_agrupation_forward(self, expression, index):
        agrupation_exp = []
        positions_move = 0
        open_agrupation_count = 0
        for i in range(index + 1, len(expression)):
            caracter = expression[i]
            if caracter == self.agrupation[0]:
                open_agrupation_count += 1
            if open_agrupation_count > 0:
                agrupation_exp.append(caracter)
            if caracter == self.agrupation[1] and open_agrupation_count > 0:
                open_agrupation_count -= 1
            if open_agrupation_count == 0:
                positions_move += 1
                break
            positions_move += 1
        return ''.join(agrupation_exp), positions_move
