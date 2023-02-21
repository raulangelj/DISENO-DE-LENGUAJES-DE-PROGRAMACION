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

	def create_token_automata(self, value: str) -> Automata:
		token_automata: Automata = Automata()
		initial_state: State = State(is_initial=True)
		final_state: State = State(True)
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


