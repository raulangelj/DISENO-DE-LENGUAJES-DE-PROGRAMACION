from Convertor.ConvertorAlgorithms import Algorithms

'''
    Convertor.py
    Class to convert the infix expression to postfix
'''
class Convertor():
    def __init__(self):
        self.value = None
        self.algorithm = Algorithms()


    def convert_from_infix_to_postfix(self, infix):
        self.value = self.algorithm.get_result_postfix(infix)
        return self.value
