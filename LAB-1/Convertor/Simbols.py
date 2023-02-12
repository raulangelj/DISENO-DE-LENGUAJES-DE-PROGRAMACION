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
		self.operators = {
			'*': 3, # kleene
			'.': 2, # concatenation
			'|': 1, # union (or)
		}
		self.agrupation = ['(', ')']

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
	