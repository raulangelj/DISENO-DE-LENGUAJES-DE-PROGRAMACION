from Automata.Token import Token
from Convertor.Operators.Constants import EMPTY_SIMBOL

class EmptyToken(Token):
	def __init__(self):
		super().__init__(EMPTY_SIMBOL)