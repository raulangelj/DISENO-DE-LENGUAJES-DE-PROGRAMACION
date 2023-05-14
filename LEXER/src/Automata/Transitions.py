from typing import Dict, List, TypedDict
from src.Automata.State import State
from src.Automata.Token import Token


class Transitions():
    def __init__(self) -> None:
        self.transitions: List[List[State, Token, State]] = []

    def add_transition(self, state: State, token: Token, next_state: State) -> None:
        self.transitions.append([state, token, next_state])

    def remove_transition(self, state: State, token: Token, next_state: State) -> None:
        self.transitions.remove([state, token, next_state])

    def get_transition(self, initial: State, token: Token) -> List[State]:
        return next(
            (
                transition[2]
                for transition in self.transitions
                if transition[0].value == initial.value
                and transition[1].value == token.value
            ),
            [],
        )

    def print_transitions(self) -> None:
        print('+---------- Transitions ----------+')
        for transition in self.transitions:
            print(
                f'{transition[0].value} --{transition[1].value}--> {transition[2].value}')
        print('+---------------------------------+')
