from typing import List
import graphviz as gv
from graphviz import Source
from Automata.Automata import Automata
from Convertor.Simbols import Operators

class NFA(Automata):
	def __init__(self) -> None:
		super().__init__()
		self.simbols: Operators = Operators()
		self.automata_stack: List[Automata] = []

	def create_automata(self, postfix:str) -> Automata:
		for caracter in postfix:
			if caracter == self.simbols.concat.get_simbol():
				automata_concat = self.simbols.concat.get_automata_rule(self.automata_stack[-2], self.automata_stack[-1])
				self.automata_stack.pop()
				self.automata_stack.pop()
				self.automata_stack.append(automata_concat)
			elif caracter == self.simbols.kleen.get_simbol():
				automata_kleen = self.simbols.kleen.get_automata_rule(self.automata_stack[-1])
				self.automata_stack.pop()
				self.automata_stack.append(automata_kleen)
			elif caracter == self.simbols.or_op.get_simbol():
				automata_or = self.simbols.or_op.get_automata_rule(self.automata_stack[-2], self.automata_stack[-1])
				self.automata_stack.pop()
				self.automata_stack.pop()
				self.automata_stack.append(automata_or)
			else:
				self.automata_stack.append(self.create_token_automata(caracter))
		self.set_automata(self.automata_stack[0])
		# self.initial_state.print_model()
		# self.final_state.print_model()
		# self.print_states()
		# self.print_alphabet()
		# self.transitions.print_transitions()
		return self

	def set_automata(self, automata: Automata) -> None:
		self.initial_state = automata.initial_state
		self.final_state = automata.final_state
		self.states = automata.states
		self.alphabet = automata.alphabet
		self.transitions = automata.transitions

	def create_graph(self, fileName: str = 'NFA') -> None:
		dot = gv.Digraph(comment='NFA Graph', format='png')
		dot.attr(rankdir='LR', size='8,5')
		# Nodes to graph
		for state in self.states:
			if state.is_final:
				dot.attr('node', shape='doublecircle')
			else:
				dot.attr('node', shape='circle')
			dot.node(str(state.value), str(state.value))
		# Edges to graph
		for state_1, token, state_2 in self.transitions.transitions:
			state_2.print_model()
			if state_2.is_final:
				dot.attr('node', shape='doublecircle')
			dot.edge(str(state_1.value), str(state_2.value), label=str(token.value))
			dot.attr('node', shape='circle')
		# doctest_mark_exe()
		dot.render(f'LAB-1/NFA_GRPAH/{fileName}.gv').replace('\\', '/')
		dot.render(f'LAB-1/NFA_GRPAH/{fileName}.gv', view=True)
		# s = Source(dot, filename='LAB-1/NFA/NFA_GRAPH.gv', format='png')
		# s.view()

	def print_states(self) -> None:
		print('+---------- States ----------+')
		for state in self.states:
			state.print_model()
		print('+-----------------------------+')

	def print_alphabet(self) -> None:
		print('+---------- Alphabet ----------+')
		for token in self.alphabet:
			token.print_token()
		print('+-------------------------------+')

