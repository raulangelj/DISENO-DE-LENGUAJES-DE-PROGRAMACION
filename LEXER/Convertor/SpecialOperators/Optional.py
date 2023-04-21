from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import OPTIONAL_SIMBOL, UNION_SIMBOL
from Convertor.Operators.Or import Or
from Convertor.Character import *
from typing import List, Tuple


class Optional(Operator):
    def __init__(self):
        super().__init__()
        self.simbol = OPTIONAL_SIMBOL
        self.or_simbol = UNION_SIMBOL
        self.priority = 3
        self.or_op = Or()
        self.errors = [
            'Invalid expresion: optional can\'t be the first simbol or follow a Union/Or operator\n',
        ]

    def evaluate(self, factors: List[Character], index: int) -> List[Character]:
        caracter_before = factors[-1].value
        new_factors = []
        open_agrupation = Character(
            value=self.agrupation[0], type=character_types.AGRUPATION)
        close_agrupation = Character(
            value=self.agrupation[1], type=character_types.AGRUPATION)
        empty = Character(value=self.empty_simbol, type=character_types.EMPTY)
        or_operator = Character(value=self.or_simbol,
                                type=character_types.OPERATOR)

        if not factors or caracter_before == self.or_simbol:
            raise Exception(self.errors[0])
        elif caracter_before is self.agrupation[1]:
            agrupation_optional, position_move = self.find_agrupation(factors)
            new_factors = [open_agrupation] + agrupation_optional + \
                [or_operator, empty, close_agrupation]
            return new_factors, position_move
        else:
            # no hay parentesis quiere decir que es algo como a?
            new_factors = [open_agrupation, factors[-1],
                           or_operator, empty, close_agrupation]
            return new_factors, 1

    def validate(self, factors, index):  # sourcery skip: raise-specific-error
        caracter_before = factors[-1] if len(factors) > 0 else ''
        if len(factors) == 0 or caracter_before is self.or_op.simbol:
            raise Exception(self.errors[0])
        # [')', actual ...]
        elif caracter_before is self.agrupation[1]:
            agrupation_optional, position_move = self.find_agrupation(factors)
            return f'{self.agrupation[0]}{agrupation_optional}{self.or_simbol}{self.empty_simbol}{self.agrupation[1]}', position_move
        # ['a|b', actual ...]
        elif len(caracter_before) > 1 and caracter_before[-1] is not self.agrupation[1]:
            letter = caracter_before[-1]
            return f'{caracter_before[:-1]}{self.agrupation[0]}{letter}{self.or_simbol}{self.empty_simbol}{self.agrupation[1]}', 1
        elif len(caracter_before) > 1:
            agrupation_optional, position_move = self.find_agrupation(
                "".join(factors))
            return f'{caracter_before[:-position_move]}{self.agrupation[0]}{agrupation_optional}{self.or_simbol}{self.empty_simbol}{self.agrupation[1]}', position_move
        else:
            return f'{self.agrupation[0]}{caracter_before}{self.or_simbol}{self.empty_simbol}{self.agrupation[1]}', 1
