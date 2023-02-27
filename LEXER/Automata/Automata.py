from __future__ import annotations
from typing import List
from Automata.State import State
from Automata.Token import Token
from Automata.Transitions import Transitions

class Automata():
	def __init__(self) -> None:
		self.initial_state: State
		self.final_state: State
		self.states: List[State] = []
		self.alphabet: List[Token] = []
		self.transitions: Transitions = Transitions()
		self.state_counter: int = 0

	def create_token_automata(self, value: str, state_counter:int) -> Automata:
		token_automata: Automata = Automata()
		initial_state: State = State(is_initial=True, value=state_counter)
		state_counter += 1
		final_state: State = State(is_final=True, value=state_counter)
		token_automata.initial_state = initial_state
		token_automata.final_state = final_state
		token: Token = Token(value)
		token_automata.states: List[State] = [token_automata.initial_state, token_automata.final_state]
		token_automata.alphabet: List[Token] = [token]
		token_automata.transitions.add_transition(initial_state, token, final_state)
		return token_automata

	def add_alphabet(self, token: Token or List[Token]) -> None:
		if type(token) is list:
			for token_item in token:
				if not token_item.is_in(self.alphabet):
					self.alphabet.append(token_item)
		elif not token.is_in(self.alphabet):
			self.alphabet.append(token)

	def remove_state(self, state: State) -> List[Token]:
		index_state = self.states.index(state)
		transitions: List[List[Token, State]] = []
		transition_to_remove: List[List[State, Token, State]] = []
		# find the position of all the transitions that have the state to remove 
		# and remove them
		for initial_state, token, final_state in self.transitions.transitions:
			if initial_state == state:
				transitions.append([token, final_state])
			if initial_state == state or final_state == state:
				transition_to_remove.append([initial_state, token, final_state])
		# remove the state from the list of states
		self.states.pop(index_state)
		# remove the transitions that have the state to remove
		for element in transition_to_remove:
			self.transitions.transitions.remove(element)
		return transitions

	def get_state_counter(self) -> int:
		self.state_counter += 1
		return self.state_counter
	
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

	def print_automata(self) -> None:
		self.initial_state.print_model()
		self.final_state.print_model()
		self.print_states()
		self.print_alphabet()
		self.transitions.print_transitions()
		


