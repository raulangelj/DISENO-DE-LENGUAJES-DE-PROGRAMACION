from termcolor import colored
from src.Convertor.ConvertorAlgorithms import Algorithms
from src.Convertor.Simbols import Operators
from src.Convertor.Character import *
from typing import List


'''
    src.Convertor.py
    Class to convert the infix expression to postfix
'''


class Parser():
    def __init__(self):
        self.postfix = None
        self.algorithm = Algorithms()
        self.operators = Operators()

    '''
        Convert the infix expression to postfix
        @param infix: infix expression (str)
        @return: postfix expression (str)
    '''

    def convert_from_infix_to_postfix(self, infix, parse=True):
        self.infix = None
        self.postfix = None
        if infix is None:
            return None
        if parse:
            infix = self.parse_expression(infix)
        self.infix = infix
        self.postfix = self.algorithm.get_result_postfix(infix)
        return self.postfix

    '''
        This function is used to parse an expression. It takes in a parameter 'expression' and attempts to evaluate the expression using the 'operators' object. If an exception is raised, it prints the exception in red and returns None.
    '''

    def parse_expression(self, expression, already_validate: bool = False):
        try:
            return self.operators.evaluate_rules(expression, already_evaluated=already_validate)
        except Exception as e:
            print(colored(e, 'red'))
            return None

    def remove_special_characters(self, infix: List[Character]) -> List[Character]:
        return self.operators.remove_special_characters(infix)

    '''
        Generate a array of caracters from the infix expression
        @param infix: infix expression (str)
        @return: array of caracters (list)
    '''

    def generate_nodes(self, infix):
        pass

    def aumented_infix(self, infix):
        return f'{infix}#'
