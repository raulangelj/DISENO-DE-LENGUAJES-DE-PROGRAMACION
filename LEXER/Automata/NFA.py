from typing import List
import graphviz as gv
from termcolor import colored
from Automata.Automata import Automata
from Automata.State import State
from Automata.Token import Token
from Automata.EmptyToken import EmptyToken
from Convertor.Simbols import Operators
from Automata.DFA import DFA

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
		dot.node('initial', 'initial', shape='point')
		for state in self.states:
			if state.is_final:
				dot.node(str(state.value), str(state.value), shape='doublecircle')
			else:
				dot.node(str(state.value), str(state.value), shape='circle')
		# Edges to graph
		dot.edge('initial', str(self.initial_state.value))
		for state_1, token, state_2 in self.transitions.transitions:
			dot.edge(str(state_1.value), str(state_2.value), label=str(token.value))
		dot.render(f'LEXER/NFA_GRAPH/{fileName}.gv', view=True)

	def e_closure(self, states: List[State]):
		e_closure = states.copy()
		for state in e_closure:
			for initial_state, token, final_state in self.transitions.transitions:
				if (
					initial_state == state
					and token.value == EmptyToken().value
					and final_state not in e_closure
				):
					e_closure.append(final_state)
		return e_closure


	def move(self, states: List[State], token_to_evaluate: Token) -> List[State]:
		move = [] + states
		for state in states:
			for initia_state, token, final_state in self.transitions.transitions:
				if (
					initia_state == state
					and token.value == token_to_evaluate.value
					and final_state not in move
				):
					move.append(final_state)
		return move
	
	def simulate(self, input_string: str) -> str:
		current_states = self.e_closure([self.initial_state])
		for caracter in input_string:
			current_states = self.e_closure(self.move(current_states, Token(caracter)))
		is_valid = any(state.is_final for state in current_states)
		if is_valid:
			return colored(f'"{input_string}" is valid', 'green')
		else:
			return colored(f'"{input_string}" is invalid', 'red')
	
	def DFA_subsets(self):
		dfa = DFA()
		temporal_states = []
		dfa_states = self.e_closure([self.initial_state])
		print('=>dfa_states: ', dfa_states)
