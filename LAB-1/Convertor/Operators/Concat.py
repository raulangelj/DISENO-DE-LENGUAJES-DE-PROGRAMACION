from Convertor.Operators.Operator import Operator
from Convertor.Operators.Constants import CONCATENATION_SIMBOL, UNION_SIMBOL


class Concat(Operator):
	def __init__(self):
		super().__init__()
		self.simbol = CONCATENATION_SIMBOL
		self.priority = 2

	'''
		Validate the expression
		@param factors: list of factors
		@param index: index of the factor to validate
		@return: expression validated (str)
	'''
	def validate(self, factors, index = 0):
		final_exp =''
		for index in range(len(factors)):
			# ['(', ...], ['a', ')'], ['a']
			if factors[index] == self.agrupation[0] or (factors[index] not in self.agrupation and factors[index + 1 if index < len(factors) - 1 else index] is self.agrupation[1]) or (index == len(factors) - 1):
				final_exp += factors[index]
			# ['a|', ...]
			elif len(factors[index]) > 1 and factors[index][-1] ==  UNION_SIMBOL:
				final_exp += factors[index]
			else:
				final_exp += f'{factors[index]}{self.simbol}'
		return final_exp, 0