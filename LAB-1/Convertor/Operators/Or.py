from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import UNION_SIMBOL, KLEENE_SIMBOL


class Or(Operator):
	def __init__(self):
		super().__init__()
		self.simbol = UNION_SIMBOL
		self.priority = 1
		self.errors = [
			'Invalid expresion: kleene can\'t be the first simbol or its second operator be a kleene/union/optional/plus.\n',
		]

	'''
		* Validate the expression and return the new expression and the number of positions to move
		@param factors: the expression to validate
		@param index: the index of the simbol to validate
		@param expression: the original expression
		@return: new expression, number of positions to move, if the move was forward true else false
	'''

	def validate(self, factors, index, expression):
		# sourcery skip: raise-specific-error
		caracter_before = factors[-1] if len(factors) > 0 else ''
		caracter_after = expression[index +
									1] if index < len(expression) - 1 else ''
		# TODO: add the plus and optional simbols to this validation
		if len(factors) == 0 or caracter_after in [self.simbol, KLEENE_SIMBOL]:
			# * can't be the first simbol or its second operator be a kleene/union/optional/plus
			raise Exception(self.errors[0])
		# [actual , '(', ...]
		elif caracter_after is self.agrupation[0]:
			agrupation_or, positions_move = self.find_agrupation(
				expression, True)
			return f'{caracter_before}{self.simbol}{agrupation_or}', positions_move, True
		# [')', actual ...]
		elif caracter_before is self.agrupation[1]:
			agrupation_or, positions_move = self.find_agrupation(
				factors, False)
			return f'{agrupation_or}{self.simbol}{caracter_after}', positions_move, False
		else:
			return f'{caracter_before}{self.simbol}{caracter_after}', 1, False
