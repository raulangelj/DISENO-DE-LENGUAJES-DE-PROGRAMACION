from Convertor.Parser import Parser
from Automata.NFA import NFA
from Automata.DFA import DFA

class Controller():
	def __init__(self) -> None:
		self.parser: Parser = Parser()
		self.nfa: NFA = NFA()
		self.dfa = DFA()

	def convert_infix_to_postfix(self, infix: str) -> str:
		self.original_infix = infix
		return self.parser.convert_from_infix_to_postfix(infix)

	def create_automata(self, postfix: str) -> NFA:
		self.nfa.create_automata(postfix, self.parser.infix, self.original_infix)
		return self.nfa

	def render_graph(self, file_name:str='') -> None:
		self.nfa.create_graph(file_name)

	def get_dfa_subsets(self) -> None:
		self.dfa = self.nfa.DFA_subsets()

	def simulate_nfa(self, input_string: str) -> str:
		return self.nfa.simulate(input_string)

	