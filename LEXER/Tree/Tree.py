
from Tree.Node import Node
from Convertor.Parser import Parser
from typing import Dict
import graphviz as gv

class Tree():
    def __init__(self, postfix: str):
        self.postfix = postfix
        self.tree = None
        self.parser: Parser = Parser()
        self.i_counter = 1
        self.followpos = {}
        self.language = []
        self.leaves: Dict[int, Node] = {}
        self.last_counter = -1
        self.dot = gv.Digraph(comment=f'{self.postfix} Tree')
        self.dot.attr(label=f'{self.postfix} Tree')

    def create_tree(self) -> None:
        stack = []
        keep_reading = True
        index = 0
        if not self.postfix:
            return
        while keep_reading:
        # for caracter in self.postfix:
        # for index in range(len(self.postfix)):
            # caracter = self.postfix[index]
            if index > len(self.postfix) - 1:
                keep_reading = False
            elif self.parser.operators.is_two_param_operator(self.postfix[index]):
                z = Node(self.postfix[index])
                right = stack.pop()
                left = stack.pop()
                z.left = left
                z.right = right
                stack.append(z)
            elif self.parser.operators.is_one_param_operator(self.postfix[index]):
                z = Node(self.postfix[index])
                left = stack.pop()
                z.left = left
                stack.append(z)
            else:
                char_value = self.postfix[index] + self.postfix[index + 1] + self.postfix[index + 2]
                if char_value == '092':
                    char_value += self.postfix[index + 3] + self.postfix[index + 4] + self.postfix[index + 5]
                    index += 3
                stack.append(Node(value=char_value, i=self.i_counter))
                if char_value not in self.language and char_value != self.parser.operators.optional.empty_simbol and char_value != '#':
                    self.language.append(char_value)
                if char_value == '#':
                    self.last_counter = self.i_counter
                self.i_counter += 1
                index += 2
            index += 1
        self.tree = stack.pop()
        print(self.tree.value)
        # self.inorder(self.tree)

    def inorder(self, x):
        if not x:
            return
        self.inorder(x.left)
        print(x.value, end=" ")
        self.inorder(x.right)

    def postorder(self, x):
        if not x:
            return
        self.postorder(x.left)
        self.postorder(x.right)
        print(x.value, end=" ")

    def render_tree(self, x):
        if x.left:
            self.dot.node(x.left.uuid, x.left.value)
            self.dot.edge(x.uuid, x.left.uuid)
            self.render_tree(x.left)
        if x.right:
            self.dot.node(x.right.uuid, x.right.value)
            self.dot.edge(x.uuid, x.right.uuid)
            self.render_tree(x.right)
        if x.uuid == self.tree.uuid:
            self.dot.node(x.uuid, x.value)
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
