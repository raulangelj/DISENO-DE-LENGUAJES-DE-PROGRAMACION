from Automata.Token import Token
from Convertor.Operators.Operator import Operator
from uuid import uuid4


class Node():
    def __init__(self, value: str = None, left: str = None, right: str = None, i=None) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.operator = Operator()
        self.i = i
        self.uuid = str(uuid4())
    
    def nullable(self) -> bool:
        if self.value == self.operator.empty_simbol:
            return True
        elif self.value == self.operator.kleene_simbol:
            return True
        elif self.value == self.operator.concatenation_simbol:
           return self.left.nullable() and self.right.nullable()
        elif self.value == self.operator.union_simbol:
            return self.left.nullable() or self.right.nullable()
        else:
            return False
        
    def firstpos(self) -> list:
        if self.value == self.operator.empty_simbol:
            return []
        elif self.value == self.operator.kleene_simbol:
            return self.left.firstpos()
        elif self.value == self.operator.concatenation_simbol:
            if self.left.nullable():
                return self.left.firstpos() + self.right.firstpos()
            else:
                return self.left.firstpos()
        elif self.value == self.operator.union_simbol:
            return self.left.firstpos() + self.right.firstpos()
        else:
            return [self.i]
    
    def lastpos(self) -> list:
        if self.value == self.operator.empty_simbol:
            return []
        elif self.value == self.operator.kleene_simbol:
            return self.left.lastpos()
        elif self.value == self.operator.concatenation_simbol:
            if self.right.nullable():
                return self.left.lastpos() + self.right.lastpos()
            else:
                return self.right.lastpos()
        elif self.value == self.operator.union_simbol:
            return self.left.lastpos() + self.right.lastpos()
        else:
            return [self.i]
