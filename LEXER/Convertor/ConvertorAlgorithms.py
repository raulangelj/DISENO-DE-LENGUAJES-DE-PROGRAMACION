from Convertor.Simbols import Operators

'''
	Class to implement the algorithms to convert
'''
class Algorithms():
	'''
		Constructor
		@param algorithm: algorithm to use (str) (default: shunting_yard)
	'''
	def __init__(self, algorithm = 'shunting_yard'):
		self.algorithm = algorithm
		self.operators_stack = []
		self.output_queue = []
		self.operators = Operators()

	'''
		Convert the infix expression to postfix
		@param infix: infix expression (str)
		@return: postfix expression (str)
	'''
	def get_result_postfix(self, infix):
		return self.shunting_yard(infix) if self.algorithm == 'shunting_yard' else None

	'''
		Convert the infix expression to postfix using the shunting yard algorithm
		@param infix: infix expression (str)
		@return: postfix expression (str)
	'''
	def shunting_yard(self, infix):
		self.operators_stack = []
		self.output_queue = []
		keep_reading = True
		index = 0
		# For each token in the infix string
		# for index in range(len(infix)):
		while keep_reading:
			# caracter = infix[index]
			if index > len(infix) - 1:
				keep_reading = False
			# If the token is not a operator or agrupation (language) then add it to the output queue
			# print('caracter: ', caracter)
			elif not self.operators.is_operator(infix[index]) and not self.operators.is_agrupation(infix[index]):
				# print('is not operator')
				char_val = infix[index] + infix[index + 1] + infix[index + 2]
				if char_val == '092':
					char_val += infix[index + 3] + infix[index + 4] + infix[index + 5]
					index += 3
				self.output_queue.append(char_val)
				# self.output_queue.append(caracter)
				# self.output_queue.append(infix[index + 1])
				# self.output_queue.append(infix[index + 2])
				index += 2
				# cambiar por while y cocntrol el index

			# If the token is a left agrupation then push it onto the operators stack
			elif self.operators.is_left_agrupation(infix[index]):
				# print('is left agrupation')
				self.operators_stack.append(infix[index])
			# If the token is a right agrupation then pop operators from the operators stack onto the output queue until the matching left agrupation is found
			elif self.operators.is_right_agrupation(infix[index]):
				# print('is right agrupation')
				while self.operators_stack and not self.operators.is_left_agrupation(self.operators_stack[-1]):
					# print('pop: ', self.operators_stack[-1])
					self.output_queue.append(self.operators_stack.pop())
				# Pop the left agrupation from the stack, but not onto the output queue
				self.operators_stack.pop()
				# print('operators_stack: ', self.operators_stack)
				# print('output_queue: ', self.output_queue)
			# If the token is an operator, then:
			else:
				# print('is operator')
				# while there is an operator at the top of the operators stack with greater or equal precedence
				# if self.operators_stack:
					# print('ultimo operador: ', self.operators_stack[-1], ' con prioridad: ', self.operators.get_operator_priority(self.operators_stack[-1]))
					# print('caracter: ', caracter, ' con prioridad: ', self.operators.get_operator_priority(caracter))
				while self.operators_stack and self.operators.get_operator_priority(self.operators_stack[-1]) >= self.operators.get_operator_priority(infix[index]):
					# print('entro al while', self.operators_stack[-1], ' >= ', caracter)
					self.output_queue.append(self.operators_stack.pop())
				# push the token onto the operators stack
				self.operators_stack.append(infix[index])
				# print('operators_stack: ', self.operators_stack)
				# print('output_queue: ', self.output_queue)
			index += 1
		# print('Se acabo el for')
		# print('operators_stack: ', self.operators_stack)
		# print('output_queue: ', self.output_queue)
		# When there are no more tokens to read:
		while self.operators_stack:
			# Pop the remaining operators from the operators stack onto the output queue
			# print('pop: ', self.operators_stack[-1], ' to output_queue')
			self.output_queue.append(self.operators_stack.pop())
		# Return the output queue as a string (postfix)
		# print('termino')
		# print('operators_stack: ', self.operators_stack)
		# print('output_queue: ', self.output_queue)
		return ''.join(self.output_queue)
