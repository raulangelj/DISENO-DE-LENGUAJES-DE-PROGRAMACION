from Convertor.Parser import Parser
from Automata.NFA import NFA

class Controller():
	def __init__(self) -> None:
		self.parser: Parser = Parser()
		self.nfa: NFA = NFA()

	def convert_infix_to_postfix(self, infix: str) -> str:
		return self.parser.convert_from_infix_to_postfix(infix)

	def create_automata(self, postfix: str) -> NFA:
		self.nfa.create_automata(postfix)
		return self.nfa

	def render_graph(self, file_name:str) -> None:
		self.nfa.create_graph(file_name)

	