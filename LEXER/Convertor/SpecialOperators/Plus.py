from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import PLUS_SIMBOL
from Convertor.Character import *
from typing import List


class Plus(Operator):
    def __init__(self):
        super().__init__()
        self.simbol = PLUS_SIMBOL
        self.priority = 3
        self.errors = [
            'Invalid expresion: plus can\'t be the first simbol or follow a Union/Or operator\n',
        ]

    def evaluate(self, factors: List[Character], index: int) -> List[Character]:
        caracter_before = factors[-1].value
        new_factors = []
        open_agrupation = Character(
            value=self.agrupation[0], type=character_types.AGRUPATION)
        close_agrupation = Character(
            value=self.agrupation[1], type=character_types.AGRUPATION)
        concatenation = Character(
            value=self.concatenation_simbol, type=character_types.OPERATOR)
        kleene = Character(value=self.kleene_simbol,
                           type=character_types.OPERATOR)

        if not factors or caracter_before is self.union_simbol:
            raise Exception(self.errors[0])
        elif caracter_before is self.agrupation[1]:
            plus_factors, move_back = self.find_agrupation(factors)
            new_factors = [open_agrupation] + plus_factors + \
                [concatenation] + plus_factors + [kleene] + [close_agrupation]
            return new_factors, move_back
        else:
            # no hay parentesis quiere decir que es algo como a+
            new_factors = [open_agrupation] + factors[-1:] + \
                [concatenation] + factors[-1:] + [kleene] + [close_agrupation]
            return new_factors, 1

    def validate(self, factors, index):  # sourcery skip: raise-specific-error
        caracter_before = factors[-1] if len(factors) > 0 else ''
        if len(factors) == 0 or caracter_before is self.union_simbol:
            raise Exception(self.errors[0])
        elif caracter_before is self.agrupation[1]:
            agrupation_plus, position_move = self.find_agrupation(factors)
            return f'{self.agrupation[0]}{agrupation_plus}{self.concatenation_simbol}{agrupation_plus}{self.kleene_simbol}{self.agrupation[1]}', position_move
        elif len(caracter_before) > 1 and caracter_before[-1] is not self.agrupation[1]:
            letter = caracter_before[-1]
            return f'{caracter_before[:-1]}{self.agrupation[0]}{letter}{self.concatenation_simbol}{letter}{self.kleene_simbol}{self.agrupation[1]}', 1
        elif len(caracter_before) > 1:
            agrupation_plus, position_move = self.find_agrupation(
                "".join(factors))
            return f'{caracter_before[:-position_move]}{self.agrupation[0]}{agrupation_plus}{self.concatenation_simbol}{agrupation_plus}{self.kleene_simbol}{self.agrupation[1]}', position_move
        else:
            return f'{self.agrupation[0]}{caracter_before}{self.concatenation_simbol}{caracter_before}{self.kleene_simbol}{self.agrupation[1]}', 1
