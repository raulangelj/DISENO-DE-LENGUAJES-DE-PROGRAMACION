from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import PLUS_SIMBOL

class Plus(Operator):
	def __init__(self):
		super().__init__()
		self.simbol = PLUS_SIMBOL
		self.priority = -1
		self.errors = [
			'Invalid expresion: plus can\'t be the first simbol or follow a Union/Or operator\n',
		]

	def validate(self, factors, index):  # sourcery skip: raise-specific-error
		caracter_before = factors[-1] if len(factors) > 0 else ''
		if len(factors) == 0 or caracter_before is self.union_simbol:
			raise Exception(self.errors[0])
		# [')', actual ...]
		elif caracter_before is self.agrupation[1]:
			agrupation_plus, position_move = self.find_agrupation(factors)
			return f'{self.agrupation[0]}{agrupation_plus}{self.concatenation_simbol}{agrupation_plus}{self.kleene_simbol}{self.agrupation[1]}', position_move
		# ['a|b', actual ...]
		elif len(caracter_before) > 1 and caracter_before[-1] is not self.agrupation[1]:
			letter = caracter_before[-1]
			return f'{caracter_before[:-1]}{self.agrupation[0]}{letter}{self.concatenation_simbol}{letter}{self.kleene_simbol}{self.agrupation[1]}', 1
		else:
			return f'{self.agrupation[0]}{caracter_before}{self.concatenation_simbol}{caracter_before}{self.kleene_simbol}{self.agrupation[1]}', 1