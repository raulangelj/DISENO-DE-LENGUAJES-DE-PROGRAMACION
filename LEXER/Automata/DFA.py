from __future__ import annotations
from Automata.Automata import Automata
from Automata.State import State
from Automata.Token import Token
from termcolor import colored
from typing import Dict, List, Tuple
from Tree.Tree import Tree
from itertools import combinations
from Convertor.Character import Characters

class tokenListModel():
    def __init__(self):
        self.characters: Characters = []
        self.accepted_state: State | None = None

class DFA(Automata):
    def __init__(self):
        super().__init__()

    def simulate(self, input_string: Characters) -> str:
        current_states = [self.initial_state]
        token_list:List[tokenListModel] = []
        word = []
        last_accepted = None
        index = 0
        last_accepted_index = -1
        start_word_index = 0
        # for caracter in input_string.characters:
        while index < len(input_string.characters):
            caracter = input_string.characters[index]
            current_states = self.move(
                current_states, Token(value=caracter.value, label=caracter.label))
            if current_states:
                word.append(caracter)
                is_valid, final_state = next(
                    ((True, state) for state in current_states if state.is_final), (False, None))
                if is_valid:
                    last_accepted = final_state
                    last_accepted_index = index
                index += 1
            elif last_accepted:
                # token_list.append([Characters(characters_list=word), last_accepted.return_value])
                tokenList = tokenListModel()
                tokenList.characters = Characters(characters_list=word[:last_accepted_index - start_word_index + 1])
                tokenList.accepted_state = last_accepted
                token_list.append(tokenList)
                word = []
                current_states = [self.initial_state]
                index = last_accepted_index + 1
                start_word_index = index
                last_accepted_index = -1
                last_accepted = None
            #     continue
            # else:
            #     return colored(f'"{input_string}" is invalid', 'red')
        # store the last value if it is valid
        if last_accepted:
            tokenList = tokenListModel()
            tokenList.characters = Characters(characters_list=word)
            tokenList.accepted_state = last_accepted
            token_list.append(tokenList)
        # print the token list characters with the retunr value of the last accepted state
        for token in token_list:
            print(token.characters, ':', token.accepted_state.return_value.value)
        return token_list  
            

                
        # is_valid = any(state.is_final for state in current_states)
        # is_valid, final_state = next(
        #     ((True, state) for state in current_states if state.is_final), (False, None))
        # if is_valid:
        #     return colored(
        #         f'"{input_string}" is valid: {final_state.return_value.value}',
        #         'green',
        #     )
        # else:
        #     return colored(f'"{input_string}" is invalid', 'red')

    def create_automata(self, postfix: str, tree: Tree, infix: str = 'DFA', originial: str = '') -> None:
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
                if next_s := list(set(next_s)):
                    if next_s not in Dstates:
                        Dstates.append(next_s)
                    Dtran.append(
                        (Dstates.index(state), simbol, Dstates.index(next_s)))
        # set the transitions and create the states
        for initial_state, token, final_state in Dtran:
            # initial state
            # is_final =  tree.last_counter in Dstates[initial_state]
            is_final, leave_index = self.is_final_state(
                Dstates[initial_state], tree)
            return_value = tree.find_final_state_data(
                leave_index) if is_final else None
            initial_state = State(
                value=initial_state, is_initial=initial_state == 0, is_final=is_final, return_value=return_value)
            self.add_state(initial_state)
            # final state
            # is_final = tree.last_counter in Dstates[final_state]
            is_final, leave_index = self.is_final_state(
                Dstates[final_state], tree)
            return_value = tree.find_final_state_data(
                leave_index) if is_final else None
            final_state = State(value=final_state,
                                is_initial=final_state == 0, is_final=is_final, return_value=return_value)
            self.add_state(final_state)
            # transition
            self.transitions.add_transition(
                initial_state, Token(token), final_state)
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
        # self.print_automata()
        return self

    def is_final_state(self, states: List[int], tree: Tree) -> Tuple(bool, str | None):
        return next(
            ((True, state) for state in states if state in tree.final_states),
            (False, None),
        )
        # return any(state in tree.final_states for state in states)

    def get_aceptance_and_noaceptance(self) -> Tuple[List[State], List[State]]:
        aceptance = []
        noaceptance = []
        for state in self.states:
            if state.is_final:
                aceptance.append(state)
            else:
                noaceptance.append(state)
        return aceptance, noaceptance

    def is_distingishable(self, state1: State, state2: State, P: List[List[State]]) -> bool:
        for token in self.alphabet:
            # see if the next position of both states is in the same group
            next_state1 = self.transitions.get_transition(state1, token)
            next_state2 = self.transitions.get_transition(state2, token)
            if (next_state1 == [] and next_state2 != []) or (next_state1 != [] and next_state2 == []):
                return True
            for group in P:
                if next_state1 != [] and next_state2 != []:
                    if (next_state1.is_in(group) and not next_state2.is_in(group)) or (next_state2.is_in(group) and not next_state1.is_in(group)):
                        return True
        return False

    def minimizing(self) -> DFA:
        aceptance, noaceptance = self.get_aceptance_and_noaceptance()
        P = [aceptance, noaceptance]
        P_new = []
        finished_minimizing = False
        while not finished_minimizing:
            P_new = []
            for group in P:
                separable = {}  # dict for distinguishable states
                # if the group is only one state add it to the p_new
                if len(group) == 1:
                    P_new.append([group[0]])
                    continue
                # creo los pares para ver si son distingibles
                # TODO arreglar la forma en la uqe veo si son distingibles, debe ser en base a los estados a los que llegan cada uno y no en base al estado que estan
                for pair in combinations(group, 2):
                    value_pair = str(pair[0].value) + str(pair[1].value)
                    state1 = self.get_state(int(pair[0].value))
                    state2 = self.get_state(int(pair[1].value))

                    separable[value_pair] = self.is_distingishable(
                        state1, state2, P)
                # for pair in combinations(group, 2):
                #     states_passed = []
                #     values_pair = ''
                #     for state in pair:
                #         values_pair += str(state.value)
                #         for token in self.alphabet:
                #             next_state = self.transitions.get_transition(state, token)
                #             if next_state not in states_passed:
                #                 states_passed.append(next_state)
                #     is_in = not all(state.is_in(group) for state in states_passed)
                #     separable[values_pair] = is_in
                print(separable)
                # Separo los grupos acorde a si son distingibles o no
                sort_orders = sorted(separable.items(), key=lambda x: x[1])
                local_groups = []
                already_added = []
                for item in sort_orders:
                    pair, value = item
                    if value:
                        for state_value in pair:
                            if state_value not in already_added:
                                state_to_add = self.get_state(int(state_value))
                                already_added.append(state_value)
                                local_groups.append([state_to_add])
                    elif pair[0] in already_added or pair[1] in already_added:
                        for mini_group in local_groups:
                            if self.get_state(int(pair[0])) in mini_group or self.get_state(int(pair[1])) in mini_group:
                                if self.get_state(int(pair[0])) not in mini_group:
                                    mini_group.append(
                                        self.get_state(int(pair[0])))
                                if self.get_state(int(pair[1])) not in mini_group:
                                    mini_group.append(
                                        self.get_state(int(pair[1])))
                                if pair[0] not in already_added:
                                    already_added.append(pair[0])
                                if pair[1] not in already_added:
                                    already_added.append(pair[1])
                    else:
                        local_groups.append(
                            [self.get_state(int(pair[0])), self.get_state(int(pair[1]))])
                        already_added.extend((pair[0], pair[1]))
                print(local_groups)
                # Add the groups to the new P
                P_new.extend(local_groups)
            if P == P_new:
                finished_minimizing = True
            P = P_new
        # Create the new automata
        new_automata = DFA()
        # Create the states
        for group in P_new:
            is_final = any(state.is_final for state in group)
            is_initial = any(state.is_initial for state in group)
            new_state = State(
                value=group[0].value, is_initial=is_initial, is_final=is_final)
            new_automata.add_state(new_state)
        # Create the transitions
        for state in new_automata.states:
            for token in self.alphabet:
                next_state = self.transitions.get_transition(
                    self.get_state(int(state.value)), token)
                for group in P_new:
                    if next_state != []:
                        if next_state.is_in(group):
                            new_next_state = new_automata.get_state(
                                int(group[0].value))
                            new_automata.transitions.add_transition(
                                state, token, new_next_state)
        # Set the alphabet
        new_automata.alphabet = self.alphabet
        # Set the initial state
        for state in new_automata.states:
            if state.is_initial:
                new_automata.initial_state = state
        # Set the final state
        for state in new_automata.states:
            if state.is_final:
                new_automata.final_state = state
        # change my self to the new automata
        self.states = new_automata.states
        self.transitions = new_automata.transitions
        self.initial_state = new_automata.initial_state
        self.final_state = new_automata.final_state
        # todo alphabet should be the same so we can remove this line
        self.alphabet = new_automata.alphabet
        return new_automata
