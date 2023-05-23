from typing import List, Dict
from src.LR.TokenSintactic import TokenSintactic
from src.LR.Production import Production
from src.LR.StateSintactic import StateSintactic, state_types
from src.LR.Transition import Transition
import graphviz as gv
from src.Tokens.Tokens import arrow, dot_ls, acceptance_simbol

first = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'),
               TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
    Production([TokenSintactic('E'), TokenSintactic(
        '-\\>'), TokenSintactic('T')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'),
               TokenSintactic('T'), TokenSintactic('*'), TokenSintactic('F')]),
    Production([TokenSintactic('T'), TokenSintactic(
        '-\\>'), TokenSintactic('F')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'),
               TokenSintactic('('), TokenSintactic('E'), TokenSintactic(')')]),
    Production([TokenSintactic('F'), TokenSintactic(
        '-\\>'), TokenSintactic('id')]),
]

second = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'),
               TokenSintactic('+'),  TokenSintactic(dot_ls), TokenSintactic('T')]),
]

# I3
third = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'),
               TokenSintactic('E'), TokenSintactic(dot_ls)]),
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'),
               TokenSintactic(dot_ls), TokenSintactic('+'), TokenSintactic('T')]),
]


class DotExpression():
    def __init__(self) -> None:
        self.index_dot: int = 0
        self.next_value: TokenSintactic = None


# **LR**
# class Lr that recieves: the first list of productions to create the LR0 automata
class Lr0():
    def __init__(self, initial_item: List[Production]) -> None:
        self.start: TokenSintactic = None
        self.transitions: List[Transition] = []
        self.states: List[StateSintactic] = []
        self.alphabet: List[TokenSintactic] = self.get_alphabet(initial_item)
        self.non_terminals: List[TokenSintactic] = self.get_non_terminals(
            initial_item)
        self.og_productions: List[Production] = initial_item
        self.create(initial_item)
        self.terminals: List[TokenSintactic] = self.get_terminals()
        self.parsing_table: Dict[int, Dict[str, str]
                                 ] = self.create_parsing_table()

    def get_terminals(self) -> List[TokenSintactic]:
        terminals = []
        for token in self.alphabet:
            if token not in self.non_terminals and token not in terminals:
                terminals.append(token)
        terminals.append(TokenSintactic(acceptance_simbol))
        return terminals

    def render_parsing_table(self) -> None:
        dot = gv.Digraph(comment='LR0', filename='LR0.gv',
                         format='pdf', node_attr={'shape': 'record'})
        actions_number = len(self.terminals)
        goto_number = len(self.non_terminals)
        table_node = f'''<
        <TABLE>
    <TR>
        <TD ROWSPAN="2">State</TD>
        <TD COLSPAN="{actions_number}">Action</TD>
        <TD COLSPAN="{goto_number}">Goto</TD>
    </TR>
    <TR>
        {"".join([f"<TD>{terminal.value}</TD>" for terminal in self.terminals])}
        {"".join([f"<TD>{non_terminal.value}</TD>" for non_terminal in self.non_terminals])}
    </TR>
    {self.get_table_rows()}
</TABLE>>'''
        dot.node('table', table_node)
        dot.render('LEXER/LR_GRAPH/LR_PARSING_TABLE.gv', view=True)

    def get_table_rows(self) -> str:
        # regresar lo de get_table_row para cada state en self.states que no sea acceptance
        return "".join([self.get_table_row(state) for state in self.states if not state.acceptance])
        # return "".join([self.get_table_row(state) for state in self.states])

    def get_table_row(self, state: StateSintactic) -> str:
        id_ = state.get_state_number()
        terminals = []
        for terminal in self.terminals:
            cell = '<TD> </TD>'
            if terminal.value in self.parsing_table[id_]:
                cell = f"<TD>{self.parsing_table[id_][terminal.value]}</TD>"
            terminals.append(cell)
        non_terminals = []
        for non_terminal in self.non_terminals:
            cell = '<TD> </TD>'
            if non_terminal.value in self.parsing_table[id_]:
                cell = f"<TD>{self.parsing_table[id_][non_terminal.value]}</TD>"
            non_terminals.append(cell)
        return f'''<TR>
        <TD>{id_}</TD>
        {"".join(terminals)}
        {"".join(non_terminals)}
    </TR>'''

    def create_parsing_table(self) -> Dict[int, Dict[str, str]]:
        parsing_table: Dict[StateSintactic, Dict[TokenSintactic, str]] = {}
        for state in self.states:
            if not state.acceptance:
                state_number = state.get_state_number()
                parsing_table[state_number] = {}
                all_items = state.items.copy() + state.clousure.copy()
                # get Shifts and acceptance
                terminals: List[TokenSintactic] = self.get_next_terminal_dot_values(
                    all_items)
                for terminal in terminals:
                    if Tj := self.get_transition(state, terminal):
                        Ij = Tj.destination
                        parsing_table[state_number][terminal.value] = self.get_shift_string(
                            Ij)
                # get reductions
                As = self.get_first_token_with_final_dot(all_items)
                for Aprod in As:
                    A = Aprod.first_token()
                    for a in self.get_follow(A):
                        parsing_table[state_number][a.value] = self.get_reduce_string(
                            Aprod)
                # go to part
                for A in self.non_terminals:
                    if Tj := self.get_transition(state, A):
                        Ij = Tj.destination
                        parsing_table[state_number][A.value] = self.get_goto_string(
                            Ij)
        print('parser table', parsing_table)
        return parsing_table

    def get_goto_string(self, state: StateSintactic) -> str:
        return f"{state.id[1:]}" if state.id[0] == 'I' else f"{state.id}"

    def get_og_production_index(self, production: Production) -> int:
        for index, og_production in enumerate(self.og_productions):
            if og_production == production:
                return index

    def get_reduce_string(self, production: Production) -> str:
        return f"r{self.get_og_production_index(production) + 1}"

    def get_first_token_with_final_dot(self, items: List[Production]) -> List[Production]:
        result_items: List[Production] = []
        for item in items:
            i = Production(item.value.copy()[:-1])
            if item.has_final_dot() and i not in result_items:
                result_items.append(i)
        return result_items

    def get_shift_string(self, state: StateSintactic) -> str:
        return f"s{state.id[1:]}" if state.id[0] == 'I' else f"{state.id}"

    def get_next_terminal_dot_values(self, items: List[Production]) -> List[TokenSintactic]:
        next_dot_values: List[TokenSintactic] = []
        for item in items:
            if next_token := item.next_token(TokenSintactic(dot_ls)):
                if next_token not in next_dot_values and next_token not in self.non_terminals:
                    next_dot_values.append(next_token)
        return next_dot_values

    def get_transition(self, origin: StateSintactic, simbol: TokenSintactic) -> Transition:
        return next(
            (
                transition
                for transition in self.transitions
                if transition.origin == origin and transition.simbol == simbol
            ),
            None,
        )

    def get_alphabet(self, initial_items: List[Production]) -> List[TokenSintactic]:
        alphabet: List[TokenSintactic] = []
        for item in initial_items:
            for token in item.value:
                if token not in alphabet and token.value != arrow:
                    alphabet.append(token)
        return alphabet

    def get_non_terminals(self, initial_items: List[Production]) -> List[TokenSintactic]:
        non_terminals: List[TokenSintactic] = []
        for item in initial_items:
            if item.first_token() not in non_terminals:
                non_terminals.append(item.first_token())
        return non_terminals

    def aumented(self, initial_items: List[Production]) -> List[Production]:
        first_expression = initial_items[0].first_token()
        return [
            Production(
                [TokenSintactic(f"{first_expression.value}'"),
                 TokenSintactic(arrow),
                 TokenSintactic(dot_ls),
                 TokenSintactic(first_expression.value), TokenSintactic(acceptance_simbol)]
            )
        ]

    def is_same_list_productions(self, first: List[Production], second: List[Production]) -> bool:
        if len(first) != len(second):
            return False
        return all(item in second for item in first)

    def is_in_list_production(self, production: Production, productions: List[List[Production]]) -> bool:
        return any(
            self.is_same_list_productions(item, production) for item in productions
        )

    def print_list_production(self, productions: List[Production]) -> None:
        print("List of productions")
        for item in productions:
            print(item)

    def new_state(self, items: List[Production]) -> StateSintactic:
        state = StateSintactic()
        state.items = items.copy()
        state.clousure = self.closure(items)
        return state

    def create(self, initial_item: List[Production]) -> None:
        id_counter = 0
        aumented = self.aumented(initial_item)
        state0 = StateSintactic()
        state0.id = f'I{id_counter}'
        id_counter += 1
        state0.items = aumented
        state0.clousure = self.closure(aumented)
        C: List[StateSintactic] = [state0]
        for I in C:
            for grammar in self.get_grammar(I.clousure):
                goto = self.goTo(I.clousure, grammar)
                new_state = self.new_state(goto)
                # print(f'\n goto with {str(grammar)}')
                # self.print_list_production(new_state.clousure)
                # print(C.index(I))
                if grammar.value == acceptance_simbol:
                    new_state.change_acceptance()
                    C.append(new_state)
                    self.transitions.append(Transition(I, new_state, grammar))
                elif len(goto) > 0 and new_state not in C:
                    id_label = f'I{id_counter}'
                    id_counter += 1
                    new_state.id = id_label
                    C.append(new_state)
                    self.transitions.append(Transition(I, new_state, grammar))
                elif new_state in C:
                    state_index = C.index(new_state)
                    state = C[state_index]
                    self.transitions.append(Transition(I, state, grammar))

        # add the states
        self.states = C

    def aumented_grammar(self, items: List[Production]) -> StateSintactic:
        first_expression = items[0].value[0]
        aumented_items = [Production(
            [
                TokenSintactic(f"{first_expression.value}'"),
                TokenSintactic('-\\>'),
                TokenSintactic(dot_ls),
                TokenSintactic(first_expression.value),
            ]
        )]
        state = StateSintactic()
        state.id = "I0"
        state.items = aumented_items

        # get the closure
        aumented_clousure = self.closure(state.items)
        state.clousure = aumented_clousure
        return state

    def goTo(self, listOfItems: List[Production], token: TokenSintactic) -> List[Production]:
        listOfItem = listOfItems.copy()
        I: List[Production] = []
        for item in listOfItem:
            index_dot = item.index_of(TokenSintactic(dot_ls))
            if (
                index_dot + 1 < len(item.value)
                and item.value[index_dot + 1].value == token.value
            ):
                temp = Production()
                temp.value = item.value.copy()
                temp.value[index_dot], temp.value[index_dot +
                                                  1] = item.value[index_dot + 1], item.value[index_dot]
                I.append(temp)
        # return self.closure(I)
        return I

    def get_grammar(self, items: List[Production]) -> List[TokenSintactic]:
        grammar: List[TokenSintactic] = []
        for item in items:
            if dot_expression := self.get_dot_expression(item.value):
                if (
                    dot_expression.next_value
                    and dot_expression.next_value not in grammar
                ):
                    grammar.append(dot_expression.next_value)
        return grammar

    def closure(self, listOfItems: List[Production]) -> List[Production]:
        J: List[Production] = listOfItems.copy()
        for item in J:
            if dot_expression := self.get_dot_expression(item.value):
                for production in self.og_productions:
                    first_token = production.first_token()
                    if (
                        dot_expression.next_value
                        and first_token.value == dot_expression.next_value.value
                    ):
                        temp = Production()
                        temp.value = production.value.copy()
                        temp.value.insert(2, TokenSintactic(dot_ls))
                        if temp not in J:
                            J.append(temp)
        return J

    def get_dot_expression(self, items: List[TokenSintactic]) -> DotExpression:
        for index, token in enumerate(items):
            if token.value == dot_ls:
                dot_expression = DotExpression()
                dot_expression.index_dot = index
                dot_expression.next_value = items[index +
                                                  1] if index + 1 < len(items) else None
                return dot_expression
        return None

    def get_first_elements(self, X: TokenSintactic) -> List[TokenSintactic]:
        first_elements: List[TokenSintactic] = []
        for production in self.og_productions:
            first_element_token = production.first_token()
            element = production.first_token_expression()
            if element != X and first_element_token == X and element not in first_elements:
                first_elements.append(element)
        return first_elements

    def get_first(self, X: TokenSintactic) -> List[TokenSintactic]:
        if X not in self.non_terminals:
            return [X]
        first_values: List[TokenSintactic] = []
        first_elements = self.get_first_elements(X)
        for element in first_elements:
            if element != X:
                first_values += self.get_first(element)
        return first_values

    def get_start_simbol(self) -> TokenSintactic:
        return self.og_productions[0].first_token()

    def get_start_production_simbol_that_ends_with(self, X: TokenSintactic) -> List[Production]:
        start_production_symbols: List[Production] = []
        already_added = []
        for production in self.og_productions:
            if production.last_token() == X and production.first_token().value not in already_added:
                start_production_symbols.append(production.first_token())
                already_added.append(production.first_token().value)
        return start_production_symbols

    def get_next_symbols(self, X: TokenSintactic) -> List[TokenSintactic]:
        next_symbols: List[TokenSintactic] = []
        already_added = []
        for production in self.og_productions:
            if X in production:
                if next_token := production.next_token(X):
                    next_symbols.append(next_token)
                    already_added.append(next_token.value)
        return next_symbols

    def get_follow(self, X: TokenSintactic) -> List[TokenSintactic]:
        # ! revisar si solo se le puede sacar follow a los no terminales
        follow_values: List[TokenSintactic] = []
        if X == self.get_start_simbol():
            follow_values += [TokenSintactic('$')]
        if start_symbols := self.get_start_production_simbol_that_ends_with(X):
            for start_symbol in start_symbols:
                if start_symbol != X:
                    follow_values += self.get_follow(start_symbol)
        if next_symbols := self.get_next_symbols(X):
            for next_symbol in next_symbols:
                if next_symbol != X:
                    follow_values += self.get_first(next_symbol)
        return follow_values

    def graph(self) -> None:
        dot = gv.Digraph(comment='LR0', filename='LR0.gv', format='pdf', node_attr={
                         'shape': 'record', 'style': 'rounded'})
        # Nodes
        for state in self.states:
            dot.node(state.id, state.state_label(), shape=state.type.name)

        # Edges
        for transition in self.transitions:
            dot.edge(transition.origin.id, transition.destination.id,
                     transition.simbol.value)
        dot.render('LEXER/LR_GRAPH/LR0.gv', view=True)
