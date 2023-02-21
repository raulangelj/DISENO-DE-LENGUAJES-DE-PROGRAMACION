from typing import Dict, List, TypedDict
from Automata.State import State
from Automata.Token import Token


class Transitions():
    def __init__(self) -> None:
        self.transitions: List[List[State, Token, State]] = []

    def add_transition(self, state: State, token: Token, next_state: State) -> None:
        self.transitions.append([state, token, next_state])

    def print_transitions(self) -> None:
        print('+---------- Transitions ----------+')
        for transition in self.transitions:
            print(f'{transition[0].value} --{transition[1].value}--> {transition[2].value}')
        print('+---------------------------------+')
