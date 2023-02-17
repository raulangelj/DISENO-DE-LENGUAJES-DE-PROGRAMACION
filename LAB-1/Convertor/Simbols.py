from collections import Counter
from Convertor.Operators.Kleene import Kleene
from Convertor.Operators.Concat import Concat
from Convertor.Operators.Or import Or

OPTIONAL_SIMBOL = '?'
EMPTY_SIMBOL = 'ε'
PLUS_SIMBOL = '+'

'''
	Class Operators
	Contains the list of operatos and their priority
'''
class Operators():
	'''
		Constructor
		List of operators and their priority
	'''
	def __init__(self):
		self.kleen = Kleene()
		self.concat = Concat()
		self.or_op = Or()
		self.operators = {
			self.kleen.get_simbol(): self.kleen.get_priority(),
			self.concat.get_simbol(): self.concat.get_priority(),
			self.or_op.get_simbol(): self.or_op.get_priority()
		}
		self.agrupation = self.kleen.get_agrupation_simbols()

	'''
		Return the priority of a operator
		@param operator: operator to get the priority (str)
		@return: priority of the operator (int)
	'''
	def get_operator_priority(self, operator):
		return -1 if self.is_agrupation(operator) else self.operators[operator]

	'''
		if value is a operator
		@param operator: operator to check (str)
		@return: True if the operator is valid, False otherwise (bool)
	'''
	def is_operator(self, operator):
		return operator in self.operators

	'''
		if value is a left agrupation
		@param operator: operator to check (str)
		@return: True if the operator is a left agrupation, False otherwise (bool)
	'''
	def is_left_agrupation(self, operator):
		return operator == self.agrupation[0]
	
	'''
		if value is a right agrupation
		@param operator: operator to check (str)
		@return: True if the operator is a right agrupation, False otherwise (bool)
	'''
	def is_right_agrupation(self, operator):
		return operator == self.agrupation[1]

	'''
		Check if the operator is a agrupation
		@param operator: operator to check (str)
		@return: True if the operator is a agrupation, False otherwise (bool)
	'''
	def is_agrupation(self, operator):
		return operator in self.agrupation

	'''
		Validate the expression
		@param expression: expression to validate (str)
		@return: expression validated (str)
	'''
	def evaluate_rules(self, expression):
		self.validate_agrupations(expression)
		factors = []
		final_exp = ''
		index = 0
		# for index, caracter in enumerate(expression):
		while index < len(expression):
			caracter = expression[index]
			if caracter is self.kleen.get_simbol():
				kleen_operator, move = self.kleen.validate(factors, index)
				del factors[-move:]
				factors.append(kleen_operator)
				# factors.append(self.kleen.validate(factors, index))
			elif caracter is self.or_op.get_simbol():
				or_operator, move, forward = self.or_op.validate(factors, index, expression)
				del factors[-move:]
				factors.append(or_operator)
				index += move if forward else 1
			else:
				factors.append(caracter)
			index += 1
		final_exp, _ = self.concat.validate(factors)
		return final_exp

	'''
		Validate the agrupations
		@param expression: expression to validate (str)
		@return: is_valid (bool)
	'''
	def validate_agrupations(self, expression):
		c = Counter(expression)
		if c[self.agrupation[0]] != c[self.agrupation[1]]:
			raise Exception('Invalid agrupation')
		return True