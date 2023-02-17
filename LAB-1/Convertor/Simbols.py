KLEENE_SIMBOL = '*'
CONCATENATION_SIMBOL = '·'
UNION_SIMBOL = '|'
OPEN_AGRUPATION_SIMBOL = '('
CLOSE_AGRUPATION_SIMBOL = ')'
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
		self.operators = {
			KLEENE_SIMBOL: 3, # kleene
			CONCATENATION_SIMBOL: 2, # concatenation
			UNION_SIMBOL: 1, # union (or)
		}
		self.agrupation = [OPEN_AGRUPATION_SIMBOL, CLOSE_AGRUPATION_SIMBOL]

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
		Return the list of the operators with out the priority
	'''
	def get_operators(self):
		return list(self.operators.keys())

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
		Return the list of agrupation simbols
	'''
	def get_agrupation_simbols(self):
		return self.agrupation
	