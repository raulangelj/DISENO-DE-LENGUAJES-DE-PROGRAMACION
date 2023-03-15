from termcolor import colored
from Convertor.ConvertorAlgorithms import Algorithms
from Convertor.Simbols import Operators

'''
    Convertor.py
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
    def convert_from_infix_to_postfix(self, infix):
        self.infix = None
        self.postfix = None
        infix = self.parse_expression(infix)
        if infix is None:
            return None
        # print(f'Infix: {infix}')
        self.infix = infix
        self.postfix = self.algorithm.get_result_postfix(infix)
        return self.postfix

    '''
        This function is used to parse an expression. It takes in a parameter 'expression' and attempts to evaluate the expression using the 'operators' object. If an exception is raised, it prints the exception in red and returns None.
    '''
    def parse_expression(self, expression):
        try:
            return self.operators.evaluate_rules(expression)
        except Exception as e:
            print(colored(e, 'red'))
            return None
        
    def aumented_infix(self, infix):
        return f'({infix})#'
    
