from Convertor.Operators.Constants import OPEN_AGRUPATION_SIMBOL, CLOSE_AGRUPATION_SIMBOL


class Operator():
	def __init__(self):
		self.simbol = ''
		self.priority = -1
		self.agrupation = [OPEN_AGRUPATION_SIMBOL, CLOSE_AGRUPATION_SIMBOL]

	def get_simbol(self):
		return self.simbol

	def get_priority(self):
		return self.priority

	def evaluate(self, expresion, index):
		return expresion

	def get_agrupation_simbols(self):
		return self.agrupation

	'''
		* Find the agrupation of the expresion
		@param expresion: the expresion to find the agrupation
		@param forward: if the agrupation is forward or backward
		@return: the agrupation expresion and the number of positions to move
	'''
	def find_agrupation(self, expresion, forward=False):
		step = 1 if forward else -1
		close_agrupation_count = 0
		start_expresion = False
		agrupation_exp = []
		positions_move = 0
		for i in range(len(expresion) - 1, -1, step):
			caracter = expresion[i]
			if caracter == self.agrupation[1]:
				start_expresion = True
				close_agrupation_count += 1
			if start_expresion:
				agrupation_exp.insert(0, caracter)
			if caracter == self.agrupation[0] and close_agrupation_count > 0:
				close_agrupation_count -= 1
				start_expresion = close_agrupation_count > 0
			if close_agrupation_count == 0:
				positions_move += 1
				break
			positions_move += 1
		# TODO: raise expection if there are more open agrupations than close agrupations
		return ''.join(agrupation_exp), positions_move
