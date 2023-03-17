from __future__ import annotations
from typing import List
from random import randint


class StateModel():
	value: int
	is_final: bool
	is_initial: bool
	transitions: dict


class State():
	def __init__(self, is_final=False, is_initial=False, value:int = randint(0, 1000)) -> None:
		self.value = value
		self.is_final = is_final
		self.is_initial = is_initial
		self.transitions = {}  # ? Se manejaran las transiciones aqui? o mejor en el automata?

	def model(self) -> StateModel:
		return {
			'value': self.value,
			'is_final': self.is_final,
			'is_initial': self.is_initial,
			'transitions': self.transitions
		}
	
	def is_in(self, array_to_evaluate: List[State]) -> bool:
		for state in array_to_evaluate:
			if self.value == state.value:
				return True

	def __str__(self) -> str:
		return f'value: {self.value}, is_final: {self.is_final}, is_initial: {self.is_initial}, transitions: {self.transitions}'

	def print_model(self) -> None:
		print("+--------------------+----------+")
		print("| State              | Value    |")
		print("+--------------------+----------+")
		print("|{:<20}|{:>10}|".format('Value', self.value))
		print("|{:<20}|{:>10}|".format('Is_initial', self.is_initial))
		print("|{:<20}|{:>10}|".format('Is_final', self.is_final))
		print("+--------------------+----------+")

	def __eq__(self, __o: object) -> bool:
		return self.value == __o.value if isinstance(__o, State) else False
