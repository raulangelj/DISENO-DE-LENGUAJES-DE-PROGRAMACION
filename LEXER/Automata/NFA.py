from typing import List
from termcolor import colored
from Automata.Automata import Automata
from Automata.State import State
from Automata.Transitions import Transitions
from Automata.Token import Token
from Automata.EmptyToken import EmptyToken
from Convertor.Simbols import Operators
from Automata.DFA import DFA

class NFA(Automata):
	def __init__(self) -> None:
		super().__init__()
		self.simbols: Operators = Operators()
		self.automata_stack: List[Automata] = []

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
	
	def simulate(self, input_string: str) -> str:
		current_states = self.e_closure([self.initial_state])
		for caracter in input_string:
			current_states = self.e_closure(self.move(current_states, Token(caracter)))
		is_valid = any(state.is_final for state in current_states)
		if is_valid:
			return colored(f'"{input_string}" is valid', 'green')
		else:
			return colored(f'"{input_string}" is invalid', 'red')
		
	def generate_state_from_Dstates(self, Dstates: List[List[State]], state_number: int, adf: DFA):
		is_final = any(state.is_final for state in Dstates[state_number])
		new_state = State(value=state_number, is_initial=state_number == 0, is_final=is_final)
		adf.add_state(new_state)
		return new_state
	
	def DFA_subsets(self):
		dfa = DFA()
		Dstates: List[List[State]] = [self.e_closure([self.initial_state])]
		Dtran = []

		for state in Dstates:
			for simbol in self.alphabet:
				U = self.e_closure(self.move(state, simbol))
				if U not in Dstates:
					Dstates.append(U)
				Dtran.append([Dstates.index(state), simbol, Dstates.index(U)])
		# set the transitions and create the states
		for initial_state, token, final_state in Dtran:
			initial_state = self.generate_state_from_Dstates(Dstates, initial_state, dfa)

			final_state = self.generate_state_from_Dstates(Dstates, final_state, dfa)
	
			dfa.transitions.add_transition(initial_state, token, final_state)
		# set the alphabet
		dfa.alphabet = self.alphabet.copy()
		# set the initial state
		dfa.initial_state = dfa.states[0]
		# set the final states
		for state in dfa.states:
			if state.is_final:
				dfa.final_state = state
		# dfa.print_automata()
		# dfa.create_graph()
		dfa.original = self.original
		return dfa
		

