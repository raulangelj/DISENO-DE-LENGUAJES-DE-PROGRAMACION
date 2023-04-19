from collections import Counter
from Convertor.Operators.Kleene import Kleene
from Convertor.Operators.Concat import Concat
from Convertor.Operators.Or import Or
from Convertor.SpecialOperators.Optional import Optional
from Convertor.SpecialOperators.Plus import Plus
from Convertor.Character import character_types, Character
from typing import List


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
		self.optional = Optional()
		self.plus = Plus()
		self.operators = {
			self.kleen.get_simbol(): self.kleen.get_priority(),
			self.concat.get_simbol(): self.concat.get_priority(),
			self.or_op.get_simbol(): self.or_op.get_priority(),
			self.optional.get_simbol(): self.optional.get_priority(),
			self.plus.get_simbol(): self.plus.get_priority()
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
	
	def is_two_param_operator(self, operator):
		return operator in [self.concat.get_simbol(), self.or_op.get_simbol()]
	
	def is_one_param_operator(self, operator):
		return operator in [self.kleen.get_simbol(), self.optional.get_simbol(), self.plus.get_simbol()]

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
	def evaluate_rules(self, expression: List[Character], concat=True, already_evaluated=False):
		# sourcery skip: raise-specific-error
		if expression is None or expression == '':
			raise Exception('Expression is empty')
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
				or_operator, move, *forward = self.or_op.validate(factors, index, expression)
				if len(forward) > 1:
					new_agrupation_evaluated = self.evaluate_rules(or_operator, False)
					or_operator, move, *forward = self.or_op.parse(new_agrupation_evaluated, positions_move=move, caracter_before=forward[1])
				del factors[-1 if forward[0] else -move:]
				factors.append(or_operator)
				index += move if forward[0] else 1
			elif caracter is self.optional.get_simbol():
				optional_operator, move = self.optional.validate(factors, index)
				del factors[-move:]
				factors.append(optional_operator)
			elif caracter is self.plus.get_simbol():
				plus_operator, move = self.plus.validate(factors, index)
				del factors[-move:]
				factors.append(plus_operator)
			else:
				factors.append(caracter)
			index += 1
		if concat:
			final_exp, _ = self.concat.validate(factors)
		else:
			final_exp = ''.join(factors)
		return factors if already_evaluated else final_exp
	
	def remove_special_characters(self, expression: List[Character]) -> List[Character]:
		new_expresion = []
		index = 0
		while index < len(expression):
			caracter = expression[index].value
			a = "".join(i.value for i in new_expresion)
			if caracter == self.plus.get_simbol():
				plus_operator, move_back = self.plus.evaluate(new_expresion, index)
				del new_expresion[-move_back:]
				new_expresion += plus_operator
			elif caracter == self.optional.get_simbol():
				optional_operator, move_back = self.optional.evaluate(new_expresion, index)
				del new_expresion[-move_back:]
				new_expresion += optional_operator
			else:
				new_expresion.append(expression[index])
			index += 1
		return new_expresion


	'''
		Validate the agrupations
		@param expression: expression to validate (str)
		@return: is_valid (bool)
	'''
	def validate_agrupations(self, expression):
		open_agrupations = []
		for index, caracter in enumerate(expression):
			if self.is_left_agrupation(caracter):
				open_agrupations.append((caracter, index))
			elif self.is_right_agrupation(caracter):
				if not open_agrupations:
					raise Exception(
						f'Invalid agrupation: missing open agrupation at position {str(index)}'
					)
				open_agrupations.pop()
		if open_agrupations:
			raise Exception(
				f'Invalid agrupation: missing close agrupation for position {str(open_agrupations[0][1])}'
			)
		return True