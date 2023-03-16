from Automata.Automata import Automata
from Automata.State import State
from Automata.Token import Token
from termcolor import colored
from typing import Dict, List
from Tree.Tree import Tree

class DFA(Automata):
    def __init__(self):
        super().__init__()

    def simulate(self, input_string: str) -> str:
        current_states = [self.initial_state]
        for caracter in input_string:
            current_states = self.move(current_states, Token(caracter))
        is_valid = any(state.is_final for state in current_states)
        if is_valid:
            return colored(f'"{input_string}" is valid', 'green')
        else:
            return colored(f'"{input_string}" is invalid', 'red')
        
    def create_automata(self, postfix: str, tree: Tree, infix:str = 'DFA', originial:str = '') -> None:
        self.infix = infix
        self.original = originial
        Dstates: List[List[int]] = [tree.tree.firstpos()]
        Dtran = []
        for state in Dstates:
            for simbol in tree.language:
                next_s = []
                for p in state:
                    if tree.leaves[p].value == simbol:
                        next_s.extend(tree.followpos[p])
                if next_s:
                    if next_s not in Dstates:
                        Dstates.append(next_s)
                    Dtran.append((Dstates.index(state), simbol, Dstates.index(next_s)))
        # set the transitions and create the states
        for initial_state, token, final_state in Dtran:
            # initial state
            is_final =  tree.last_counter in Dstates[initial_state]
            initial_state = State(value=initial_state, is_initial=initial_state == 0, is_final=is_final)
            self.add_state(initial_state)
            # final state
            is_final =  tree.last_counter in Dstates[final_state]
            final_state = State(value=final_state, is_initial=final_state == 0, is_final=is_final)
            self.add_state(final_state)
            # transition
            self.transitions.add_transition(initial_state, Token(token), final_state)
        # set the alphabet
        alphabet: List[Token] = [Token(token) for token in tree.language]
        self.alphabet = alphabet
        # set the initial state
        for state in self.states:
            if state.value == 0:
                self.initial_state = state
        # set the final states
        for state in self.states:
            if state.is_final:
                self.final_state = state
        self.print_automata()
        return self


