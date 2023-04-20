from Convertor.Character import Character, character_types
from Tree.Node import Node
from Convertor.Parser import Parser
from typing import Dict, List
from YALEX.YALEX import ReturnModel
import graphviz as gv

class Tree():
    def __init__(self, postfix: List[Character], rules: List[ReturnModel] = None):
        if rules is None:
            rules = []
        self.postfix = postfix
        self.tree = None
        self.parser: Parser = Parser()
        self.i_counter = 1
        self.followpos = {}
        self.language = []
        self.leaves: Dict[int, Node] = {}
        self.final_states = []
        self.dot = gv.Digraph(comment=f'{self.get_postfix()} Tree')
        self.dot.attr(label=f'{self.get_postfix()} Tree')
        self.rules = rules

    def create_tree(self) -> None:
        stack = []
        final_states_counter = 0
        if not self.postfix:
            return
        for simbol in self.postfix:
            caracter = simbol.value
            if self.parser.operators.is_two_param_operator(caracter):
                z = Node(value=caracter, type=simbol.type, label=simbol.label)
                right = stack.pop()
                left = stack.pop()
                z.left = left
                z.right = right
                stack.append(z)
            elif self.parser.operators.is_one_param_operator(caracter):
                z = Node(value=caracter, type=simbol.type, label=simbol.label)
                left = stack.pop()
                z.left = left
                stack.append(z)
            else:
                stack.append(Node(value=caracter, i=self.i_counter, type=simbol.type, label=simbol.label))
                if caracter not in self.language and caracter != self.parser.operators.optional.empty_simbol and caracter != '#':
                    self.language.append(caracter)
                if caracter == '#':
                    self.final_states.append(self.i_counter)
                    if self.rules:
                        self.rules[final_states_counter].leave_index = self.i_counter
                    final_states_counter += 1
                self.i_counter += 1
        self.tree = stack.pop()
        # print(self.tree.value)
        # self.inorder(self.tree)
    
    def find_final_state_data(self, leave_id: int) -> ReturnModel:
        return next(
            (rule for rule in self.rules if rule.leave_index == leave_id), None
        )


    def inorder(self, x):
        if not x:
            return
        self.inorder(x.left)
        # print(x.value, end=" ")
        self.inorder(x.right)

    def postorder(self, x):
        if not x:
            return
        self.postorder(x.left)
        self.postorder(x.right)
        # print(x.value, end=" ")

    def render_tree(self, x):
        if x.left:
            label = x.left.value + '\n' + x.left.label if x.left.type == character_types.SIMBOL else x.left.value 
            self.dot.node(x.left.uuid, label)
            self.dot.edge(x.uuid, x.left.uuid)
            self.render_tree(x.left)
        if x.right:
            label = x.right.value + '\n' + x.right.label if x.right.type == character_types.SIMBOL else x.right.value
            self.dot.node(x.right.uuid, label)
            self.dot.edge(x.uuid, x.right.uuid)
            self.render_tree(x.right)
        if x.uuid == self.tree.uuid:
            label = x.label + '\n' + x.label if x.type == character_types.SIMBOL else x.value
            self.dot.node(x.uuid, label)
            self.dot.render('LEXER/output/tree.gv', view=True)
        
    
    def followpos_recursive(self, x: Node):
        if not x:
            return
        self.followpos_recursive(x.left)
        self.followpos_recursive(x.right)
        # print(x.value, end=" ")
        if x.value == self.parser.operators.kleen.simbol:
            for i in x.lastpos():
                if i not in self.followpos:
                    self.followpos[i] = []
                self.followpos[i] += x.firstpos()
        elif x.value == self.parser.operators.concat.simbol:
            for i in x.left.lastpos():
                if i not in self.followpos:
                    self.followpos[i] = []
                self.followpos[i] += x.right.firstpos()
        if x.left is None and x.right is None:
            self.leaves[x.i] = x

    def followpos(self) -> None:
        followpos = {}
        # iterate my tree 

    def get_postfix(self) -> str:
        return ''.join(character.label for character in self.postfix)