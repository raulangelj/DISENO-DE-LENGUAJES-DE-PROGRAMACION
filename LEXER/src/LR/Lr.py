from typing import List
from src.LR.TokenSintactic import TokenSintactic
from src.LR.Production import Production
from src.LR.StateSintactic import StateSintactic
from src.LR.Transition import Transition
import graphviz as gv
from src.Tokens.Tokens import arrow, dot_ls


# simpleState1 = StateSintactic()
# simpleState1.id = 'I0'
# simpleState1.items = [
#     Production([TokenSintactic('S'), TokenSintactic('-\\>'), TokenSintactic('E')]),
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('T')]),
# ]
# simpleState1.clousure = [
#     Production([TokenSintactic('S'), TokenSintactic('-\\>'), TokenSintactic('E')]),
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
# ]

# simpleState2 = StateSintactic()
# simpleState2.id = 'I1'
# simpleState2.items = [
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('T')]),
#     Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('T'), TokenSintactic('*'), TokenSintactic('F')]),
# ]
# simpleState2.clousure = [
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
#     Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('T')]),
#     Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('T'), TokenSintactic('*'), TokenSintactic('F')]),
#     Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('F')]),
# ]

first = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('T')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('T'), TokenSintactic('*'), TokenSintactic('F')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('F')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'), TokenSintactic('('), TokenSintactic('E'), TokenSintactic(')')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'), TokenSintactic('id')]),
]

second = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'),  TokenSintactic(dot_ls) , TokenSintactic('T')]),
]

class DotExpression():
    def __init__(self) -> None:
        self.index_dot: int = 0
        self.next_value: TokenSintactic = None



# **LR**
# - terminals: List[TokenSintactic]
# - non_terminals: List[TokenSintactic]
# - start: TokenSintactic
# - transitions: List[Transition]
# - states: List[StateSintactic]
# class Lr that recieves: the first list of productions to create the LR0 automata
class Lr0():
    def __init__(self, initial_item: List[Production]) -> None:
        self.non_terminals: List[TokenSintactic] = []
        self.start: TokenSintactic = None
        self.transitions: List[Transition] = []
        self.states: List[StateSintactic] = []
        # self.create(initial_item)
        # ! change for initial item
        self.terminals: List[TokenSintactic] = self.get_terminals(first)
        self.og_productions: List[Production] = first
        self.create(first)

    def get_terminals(self, initial_items: List[Production]) -> List[TokenSintactic]:
        terminals: List[TokenSintactic] = []
        for item in initial_items:
            if item.first_token() not in terminals:
                terminals.append(item.first_token())
        return terminals

    def create(self, initial_item: List[Production]) -> None:
        # do the aumented and create the first state
        I0 = self.aumented_grammar(initial_item)
        self.states.append(I0)
        state_dummy = StateSintactic()
        state_dummy.id = "I7"
        state_dummy.items = second
        state_dummy.clousure = self.closure(state_dummy.items)
        self.states.append(state_dummy)




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
        # # aumented_clousere will have a list of productions just as items but after the the arrow string from tokens will add the dto_ls string
        # aumented_clousure = []
        # for item in items:
        #     tempProduction = Production()
        #     for index, token in enumerate(item.value):
        #         tempProduction.value.append(token)
        #         if index == 1:
        #             tempProduction.value.append(arrow)
        #     aumented_clousure.append(tempProduction)
        # create the new state

        # state.clousure = aumented_clousure
        return state
    
    def closure(self, listOfItems: List[Production]) -> List[Production]:
        J:List[Production] = listOfItems.copy()
        for item in J:
            dot_expression = self.get_dot_expression(item.value)
            if dot_expression:
                for production in self.og_productions:
                    first_token = production.first_token()
                    if first_token.value == dot_expression.next_value.value:
                        temp = Production()
                        temp.value = production.value.copy()
                        temp.value.insert(2, TokenSintactic(dot_ls))
                        if temp not in J:
                            J.append(temp)
        return J
        # closure:List[Production] = []
        # dot_expression = self.get_dot_expression(state.items)
        # # if all the dot_expression.next_value are no_terminals then return the closure
        # if all(dot.next_value in self.non_terminals for dot in dot_expression):
        #     return closure
        # continue_token = TokenSintactic('')
        # for dot_next_val in dot_expression:
        #     for index, item in enumerate(self.og_productions):
        #         first_token = item.first_token()
        #         if first_token.value == dot_next_val.next_value.value or first_token.value == continue_token.value:
        #             temp = Production()
        #             temp.value = item.value.copy()
        #             # temp.value.pop(dot_next_val.index_dot)
        #             temp.value.insert(dot_next_val.index_dot, TokenSintactic(dot_ls))
        #             closure.append(temp)
        #             continue_token = item.last_token() if item.last_token() in self.terminals else continue_token
        #         if first_token.value != dot_next_val.next_value.value:
        #             dot_next_val.next_value = first_token
        # # for index, item in enumerate(state.items):
        # #     temp = Production()
        # #     temp.value = item.value.copy()
        # #     temp.value[index].pop(dot_expression[index].index_dot)
        # #     temp.value[index].insert(dot_expression[index].index_dot + 1, dot_ls)
        # #     closure.append(temp)
        # return closure

    # def get_dot_expression(self, items: List[Production]) -> List[DotExpression]:
    #     dot_expressions: List[DotExpression] = []
    #     for item in items:
    #         for index, token in enumerate(item.value):
    #             if token.value == dot_ls:
    #                 dot_expression = DotExpression()
    #                 dot_expression.index_dot = index
    #                 dot_expression.next_value =  item.value[index + 1] if index + 1 < len(item.value) else None
    #                 dot_expressions.append(dot_expression)
    #     return dot_expressions

    def get_dot_expression(self, items: List[TokenSintactic]) -> List[DotExpression]:
        # dot_expressions: List[DotExpression] = []
        for index, token in enumerate(items):
            if token.value == dot_ls:
                dot_expression = DotExpression()
                dot_expression.index_dot = index
                dot_expression.next_value =  items[index + 1] if index + 1 < len(items) else None
                return dot_expression
                # dot_expressions.append(dot_expression)
        return None




    def graph(self) -> None:
        # # ! MOCK borrar
        # self.states = [simpleState1, simpleState2]
        # self.transitions = [
        #     Transition(simpleState1, simpleState2, TokenSintactic('E')),
        # ]

        dot = gv.Digraph(comment='LR0', filename='LR0.gv', format='pdf', node_attr={'shape': 'record', 'style': 'rounded'})
        # dot.attr(rankdir='LR')
        # Nodes
        for state in self.states:
            dot.node(state.id, state.state_label())
        
        # Edges
        for transition in self.transitions:
            dot.edge(transition.origin.id, transition.destination.id, transition.simbol.value)

        dot.render('LEXER/LR_GRAPH/LR0.gv', view=True)