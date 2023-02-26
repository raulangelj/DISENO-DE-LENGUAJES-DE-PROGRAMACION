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
		self.infix: str = ''
		self.original: str = ''

	def create_automata(self, postfix:str, infix:str='NFA', original:str = '') -> Automata:
		self.infix = infix
		self.original = original
		for caracter in postfix:
			if caracter == self.simbols.concat.get_simbol():
				automata_concat = self.simbols.concat.get_automata_rule(self.automata_stack[-2], self.automata_stack[-1])
				self.add_to_automata_stack(automata_concat)
			elif caracter == self.simbols.kleen.get_simbol():
				automata_kleen = self.simbols.kleen.get_automata_rule(self.automata_stack[-1], state_counter=self.get_state_counter())
				self.automata_stack.pop()
				self.automata_stack.append(automata_kleen)
				self.state_counter += 1
			elif caracter == self.simbols.or_op.get_simbol():
				automata_or = self.simbols.or_op.get_automata_rule(self.automata_stack[-2], self.automata_stack[-1], state_counter=self.get_state_counter())
				self.add_to_automata_stack(automata_or)
				self.state_counter += 1
			else:
				self.automata_stack.append(self.create_token_automata(caracter, self.get_state_counter()))
				self.state_counter += 1
		self.set_automata(self.automata_stack[0])
		self.print_automata()
		return self

	def add_to_automata_stack(self, automata: Automata) -> None:
		self.automata_stack.pop()
		self.automata_stack.pop()
		self.automata_stack.append(automata)

	def set_automata(self, automata: Automata) -> None:
		self.initial_state = automata.initial_state
		self.final_state = automata.final_state
		self.states = automata.states
		self.alphabet = automata.alphabet
		self.transitions = automata.transitions

	def create_graph(self, fileName: str = 'NFA') -> None:
		fileName = 'NFA' if not fileName or fileName is None else fileName
		dot = gv.Digraph(comment='NFA Graph')
		dot.attr(rankdir='LR', label=f'NFA Graph: {self.original}')
		dot.engine = 'dot'
		# Nodes to graph
		for state in self.states:
			if state.is_final:
				dot.node(str(state.value), str(state.value), shape='doublecircle')
			elif state.is_initial:
				dot.node(str(state.value), str(state.value), shape='point')
			else:
				dot.node(str(state.value), str(state.value), shape='circle')
		# Edges to graph
		for state_1, token, state_2 in self.transitions.transitions:
			if state_2.is_final:
				dot.attr('node', shape='doublecircle')
			dot.edge(str(state_1.value), str(state_2.value), label=str(token.value))
			dot.attr('node', shape='circle')
		# doctest_mark_exe()
		dot.render(f'LAB-1/NFA_GRAPH/{fileName}.gv').replace('\\', '/')
		dot.render(f'LAB-1/NFA_GRAPH/{fileName}.gv', view=True)
		# s = Source(dot, filename='LAB-1/NFA/NFA_GRAPH.gv', format='png')
		# s.view()


