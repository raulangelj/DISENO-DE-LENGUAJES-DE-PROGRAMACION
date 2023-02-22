from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import OPTIONAL_SIMBOL, UNION_SIMBOL
from Convertor.Operators.Or import Or

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

	def validate(self, factors, index):  # sourcery skip: raise-specific-error
		caracter_before = factors[-1] if len(factors) > 0 else ''
		if len(factors) == 0 or caracter_before is self.or_op.simbol:
			raise Exception(self.errors[0])
		# [')', actual ...]
		elif caracter_before is self.agrupation[1]:
			agrupation_optional, position_move = self.find_agrupation(factors)
			return f'{self.agrupation[0]}{agrupation_optional}{self.or_simbol}{self.empty_simbol}{self.agrupation[1]}', position_move
		else:
			return f'{self.agrupation[0]}{caracter_before}{self.or_simbol}{self.empty_simbol}{self.agrupation[1]}', 1