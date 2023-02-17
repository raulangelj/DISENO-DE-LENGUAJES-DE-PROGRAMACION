from termcolor import colored
from Convertor.ConvertorAlgorithms import Algorithms
from Convertor.Simbols import Operators

'''
    Convertor.py
    Class to convert the infix expression to postfix
'''
class Convertor():
    def __init__(self):
        self.value = None
        self.algorithm = Algorithms()
        self.operators = Operators()


    '''
        Convert the infix expression to postfix
        @param infix: infix expression (str)
        @return: postfix expression (str)
    '''
    def convert_from_infix_to_postfix(self, infix):
        infix = self.parse_expression(infix)
        if infix is None:
            return None
        print(f'Infix: {infix}')
        self.value = self.algorithm.get_result_postfix(infix)
        return self.value

    '''
        This function is used to parse an expression. It takes in a parameter 'expression' and attempts to evaluate the expression using the 'operators' object. If an exception is raised, it prints the exception in red and returns None.
    '''
    def parse_expression(self, expression):
        try:
            return self.operators.evaluate_rules(expression)
        except Exception as e:
            print(colored(e, 'red'))
            return None
    
