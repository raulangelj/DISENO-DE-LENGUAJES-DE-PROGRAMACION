from Convertor.Parser import Parser
from Tree.Tree import Tree
from Automata.NFA import NFA
from Automata.DFA import DFA

class Controller():
	def __init__(self) -> None:
		self.parser: Parser = Parser()
		self.nfa: NFA = NFA()
		self.dfa = DFA()
		self.original_infix = ''
		self.tree: Tree = None

	def convert_infix_to_postfix(self, infix: str, aumented:bool=False) -> str:
		if aumented:
			infix = self.parser.aumented_infix(infix)
		self.original_infix = infix
		self.parser.convert_from_infix_to_postfix(infix)
		self.create_tree(self.parser.postfix)
		return self.parser.postfix

	def create_automata(self, postfix: str) -> NFA:
		self.nfa.create_automata(postfix, self.parser.infix, self.original_infix)
		return self.nfa
	
	def create_adf_direct(self) -> DFA:
		self.tree.followpos_recursive(self.tree.tree)
		self.dfa.create_automata(postfix=self.parser.postfix, tree=self.tree, infix=self.parser.infix, originial=self.original_infix)
		return self.dfa

	def reset_adf(self) -> None:
		self.dfa = DFA()

	def render_graph(self, file_name:str='', dfa:bool = False) -> None:
		if dfa:
			self.dfa.create_graph(file_name)
		else:
			self.nfa.create_graph(file_name)

	def get_dfa_subsets(self) -> None:
		self.dfa = self.nfa.DFA_subsets()

	def simulate_nfa(self, input_string: str) -> str:
		return self.nfa.simulate(input_string)
	
	def simulate_dfa(self, input_string: str) -> str:
		return self.dfa.simulate(input_string)
	
	def create_tree(self, postfix: str) -> None:
		tree = Tree(postfix)
		tree.create_tree()
		self.tree = tree

	def minimize_dfa(self) -> None:
		self.dfa.minimizing()

	