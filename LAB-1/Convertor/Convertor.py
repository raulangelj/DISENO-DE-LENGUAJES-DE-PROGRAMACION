from Convertor.ConvertorAlgorithms import Algorithms
from Convertor.Simbols import Operators, KLEENE_SIMBOL, CLOSE_AGRUPATION_SIMBOL, OPEN_AGRUPATION_SIMBOL, CONCATENATION_SIMBOL, OPTIONAL_SIMBOL, EMPTY_SIMBOL, PLUS_SIMBOL, UNION_SIMBOL

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
        infix = self.preprocess_expression(infix)
        print(f'Infix: {infix}')
        self.value = self.algorithm.get_result_postfix(infix)
        return self.value

    '''
        Evaluate if the character is not the last 
        @param expression: expression to evaluate (str)
        @param index: index of the character to evaluate (int)
        @return: True if the character is not the last and the next is not a operator, False otherwise (bool)
    '''
    def is_not_last_and_next_is_not_operator(self, expression, index):
        return index + 1 < len(expression) and expression[index + 1] not in self.operators.get_operators()

    '''
        Preprocess the expression to add concatenation (.) if it is needed
        Change (?) to (|ε)
        @param expression: expression to preprocess (str)
        @return: expression preprocessed (str)
    '''
    def preprocess_expression(self, expression):
        # Evalute the expression, if we have kleen star (*) and then we have something else we need to add a concatenation (·)
        # Example: a*b -> a*.b
        new_expression = ''
        for index, caracter in enumerate(expression):
            # * optinal simbol (?)
            if caracter == OPTIONAL_SIMBOL:
                # check if the caracter before ? is a close agrupation
                if expression[index - 1] == CLOSE_AGRUPATION_SIMBOL:
                    # iterate over the expression backwards to find the open agrupation
                    exp = self.find_expresion(expression[:index])
                    start_index = new_expression[:].rfind(exp)
                    new_expression = f'{new_expression[:start_index]}{OPEN_AGRUPATION_SIMBOL}{exp}{UNION_SIMBOL}{EMPTY_SIMBOL}{CLOSE_AGRUPATION_SIMBOL}{CONCATENATION_SIMBOL if self.is_not_last_and_next_is_not_operator(expression, index) and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL else ""}'
                if expression[index - 1] in self.operators.get_simbols():
                    exp = self.find_expresion(new_expression)
                    start_index = new_expression[:].rfind(exp)
                    new_expression = f'{new_expression[:start_index]}{OPEN_AGRUPATION_SIMBOL}{exp}{UNION_SIMBOL}{EMPTY_SIMBOL}{CLOSE_AGRUPATION_SIMBOL}{CONCATENATION_SIMBOL if self.is_not_last_and_next_is_not_operator(expression, index) and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL else ""}'
                else:
                    # IF the caracter before ? is not a close agrupation WE NEED TO ADD A OPEN AGRUPATION SIMBOL BEFORE THE CARACTER AND ADD (|ε) AFTER THE CARACTER AND A CLOSE AGRUPATION SIMBOL
                    letter = expression[index - 1]
                    start_index = new_expression[:].rfind(letter)
                    new_expression = f'{new_expression[:start_index]}{OPEN_AGRUPATION_SIMBOL}{letter}{UNION_SIMBOL}{EMPTY_SIMBOL}{CLOSE_AGRUPATION_SIMBOL}{CONCATENATION_SIMBOL if self.is_not_last_and_next_is_not_operator(expression, index) and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL else ""}'
            # * Plus simbol (+)
            elif caracter == PLUS_SIMBOL:
                # check if the caracter before ? is a close agrupation
                if expression[index - 1] == CLOSE_AGRUPATION_SIMBOL:
                    # iterate over the expression backwards to find the open agrupation
                    exp = self.find_expresion(expression[:index])
                    start_index = new_expression[:].rfind(exp)
                    new_expression = f'{new_expression[:start_index]}{OPEN_AGRUPATION_SIMBOL}{exp}{CONCATENATION_SIMBOL}{exp}{KLEENE_SIMBOL}{CLOSE_AGRUPATION_SIMBOL}{CONCATENATION_SIMBOL if self.is_not_last_and_next_is_not_operator(expression, index) and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL else ""}'
                    # new_expression += f'{exp}{KLEENE_SIMBOL}'
                elif expression[index - 1] in self.operators.get_simbols():
                    # iterate over the expression backwards to find the open agrupation
                    exp = self.find_expresion(new_expression)
                    start_index = new_expression[:].rfind(exp)
                    new_expression = f'{new_expression[:start_index]}{OPEN_AGRUPATION_SIMBOL}{exp}{CONCATENATION_SIMBOL}{exp}{KLEENE_SIMBOL}{CLOSE_AGRUPATION_SIMBOL}'
                else:
                    # IF the caracter before ? is not a close agrupation WE NEED TO ADD A OPEN AGRUPATION SIMBOL BEFORE THE CARACTER AND ADD (|ε) AFTER THE CARACTER AND A CLOSE AGRUPATION SIMBOL
                    letter = expression[index - 1]
                    start_index = start_index = new_expression[:].rfind(letter)
                    new_expression = f'{new_expression[:start_index]}{OPEN_AGRUPATION_SIMBOL}{letter}{CONCATENATION_SIMBOL}{letter}{KLEENE_SIMBOL}{CLOSE_AGRUPATION_SIMBOL}{CONCATENATION_SIMBOL if self.is_not_last_and_next_is_not_operator(expression, index) and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL else ""}'
                    # new_expression += f'{letter}{KLEENE_SIMBOL}'
            # * (kleene simbol)
            # validation to add a concatenation (·) after kleene star (*) if it is not the last caracter and the next caracter is not a operator and the next caracter is not a agrupation
            elif (
                caracter == KLEENE_SIMBOL
                and self.is_not_last_and_next_is_not_operator(expression, index)
                and expression[index + 1] is not CLOSE_AGRUPATION_SIMBOL # next caracter is not a agrupation
            ):
                new_expression += f'{caracter}{CONCATENATION_SIMBOL}'
            # * between two letters
            elif (
                caracter not in self.operators.get_operators() # current caracter is not a operator
                and caracter not in self.operators.get_agrupation_simbols() # current caracter is not a agrupation
                and self.is_not_last_and_next_is_not_operator(expression, index)
                and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL # next caracter is not a close agrupation
            ):
                new_expression += f'{caracter}{CONCATENATION_SIMBOL}'
            # * AFTER a close agrupation
            elif (
                caracter is self.operators.get_agrupation_simbols()[1] # current caracter is a close agrupation
                and self.is_not_last_and_next_is_not_operator(expression, index)
                and expression[index + 1] != CLOSE_AGRUPATION_SIMBOL # next caracter is not a close agrupation
            ):
                new_expression += f'{caracter}{CONCATENATION_SIMBOL}'
            else:
                new_expression += caracter
        return new_expression

    def find_expresion(self, expression):
        exp = []
        close_agrupation_count = 0
        start_expresion = False
        # iterate over the expression backwards to find the open agrupation
        for _, caracter_backwards in enumerate(expression[::-1]):
            if caracter_backwards == CLOSE_AGRUPATION_SIMBOL:
                start_expresion = True
                close_agrupation_count += 1
            if start_expresion:
                exp.insert(0, caracter_backwards)
            if caracter_backwards == OPEN_AGRUPATION_SIMBOL:
                close_agrupation_count -= 1
                start_expresion = close_agrupation_count > 0
        expression = ''.join(exp)
        return self.preprocess_expression(expression)
