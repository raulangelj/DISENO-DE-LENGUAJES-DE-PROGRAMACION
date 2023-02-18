from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import KLEENE_SIMBOL, UNION_SIMBOL


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
