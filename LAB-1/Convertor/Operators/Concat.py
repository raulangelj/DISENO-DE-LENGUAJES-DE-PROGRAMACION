from Convertor.Operators.Operator import Operator
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

	def validate(self, factors, index=0):
		final_exp = ''
		for index in range(len(factors)):
			is_open_agrupation = factors[index] == self.agrupation[0]
			is_not_two_agrupation_together = (
				factors[index] not in self.agrupation and factors[index + 1 if index < len(factors) - 1 else index] is self.agrupation[1])
			is_last_factor = index == len(factors) - 1
			has_more_than_one_factor = len(factors) > 1
			# ['(', ...], ['a', ')'], ['a']
			if (is_open_agrupation or is_not_two_agrupation_together or is_last_factor) and has_more_than_one_factor:
				final_exp += factors[index]
			# [')', ...]
			elif factors[index] == self.agrupation[1] and factors[index + 1 if index < len(factors) - 1 else index] in self.simbols:
				final_exp += factors[index]
			# ['a|', ...]
			elif len(factors[index]) > 1 and factors[index][-1] == UNION_SIMBOL:
				final_exp += factors[index]
			# ['(aa)', ...]
			elif len(factors[index]) > 1 and factors[index][0] == self.agrupation[0] and factors[index][-1] == self.agrupation[1]:
				final_exp += f'{self.rules_concat(factors[index])}{self.simbol if index < len(factors) - 1 else ""}'
			# ['a']
			elif index == len(factors) - 1:
				final_exp += factors[index]
			else:
				final_exp += f'{factors[index]}{self.simbol}'
		return final_exp, 0

	def rules_concat(self, agrupation):
		expresion_concat = ''
		for index in range(len(agrupation)):
			caracter = agrupation[index]
			next_index = index + 1 if index < len(agrupation) - 1 else index
			if self.is_close_open_agrupation(caracter, agrupation[next_index]) or self.is_two_letters(caracter, agrupation[next_index]):
				expresion_concat += f'{caracter}{self.simbol}'
			else:
				expresion_concat += caracter
		return expresion_concat

	def is_close_open_agrupation(self, caracter, next_caracter):
		return caracter is self.agrupation[1] and next_caracter is self.agrupation[0]

	def is_simbol(self, caracter):
		return caracter in self.simbols + self.agrupation
	
	def is_two_letters(self, caracter, next_caracter):
		return not self.is_simbol(caracter) and not self.is_simbol(next_caracter)
