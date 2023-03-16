
from Tree.Node import Node
from Convertor.Parser import Parser
from typing import Dict

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

    def create_tree(self) -> None:
        stack = []
        if not self.postfix:
            return
        for caracter in self.postfix:
            if self.parser.operators.is_two_param_operator(caracter):
                z = Node(caracter)
                right = stack.pop()
                left = stack.pop()
                z.left = left
                z.right = right
                stack.append(z)
            elif self.parser.operators.is_one_param_operator(caracter):
                z = Node(caracter)
                left = stack.pop()
                z.left = left
                stack.append(z)
            else:
                stack.append(Node(value=caracter, i=self.i_counter))
                if caracter not in self.language and caracter != self.parser.operators.optional.empty_simbol and caracter != '#':
                    self.language.append(caracter)
                if caracter == '#':
                    self.last_counter = self.i_counter
                self.i_counter += 1
        self.tree = stack.pop()
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
