from typing import List
from Convertor.Simbols import Operators

LINE_CLOSING = '\n'

class Yalex():
    def __init__(self, file_to_read: str) -> None:
        self.file_to_read = file_to_read
        self.variables = {}
        self.operators = Operators()

    def read_file(self) -> None:
        with open(self.file_to_read, 'r') as file:
            for line in file:
                word = ''
                for char in line:
                    word += char
                    if word == 'let ':
                        self.variable_declaration(line[4:]) # 4 because we already read the 'let ' word
                        word = ''
                        break
        return self.variables

    def variable_declaration(self, line: str) -> None:
        keep_reading = True
        # index_to_read = 4 # 3 because we already read the 'let ' word
        index_to_read = 0
        variable_name = ''
        # find the variable name
        while keep_reading:
            if line[index_to_read] == ' ':
                keep_reading = False
            else:
                variable_name += line[index_to_read]
                index_to_read += 1
        # find the variable value
        yalex_var, _, convert = self.expect_yalex_var(line[index_to_read + 3:]) # 3 because we already read the ' = ' word
        self.variables[variable_name] = self.convert_to_expression(yalex_var) if convert else "".join(yalex_var)
        # keep_reading = True
        # index_to_read += 1
        # variable_value = ''
        # while keep_reading:
        #     if line[index_to_read] == '\n':
        #         keep_reading = False
        #     else:
        #         variable_value += line[index_to_read]
        #         index_to_read += 1
    
    def convert_to_expression(self, variable: List[str]) -> str:
        # return f'({"|".join(variable)})'

        # final_value = '('
        # for index in range(len(variable) + 1):
        #     c = variable[index]
        #     if c in self.operators.agrupation:
        #         final_value += c
        #     elif index > len(variable) - 1 and variable[index + 1] in self.operators.agrupation:
        #         final_value += c                
        #     else:
        #         final_value += f'{c}|'
        # final_value += ')'
        # return final_value

        result = ''
        for i in range(len(variable)):
            if variable[i] == '(' or variable[i] == ')' or i == len(variable) - 2:
                result += variable[i]
            else:
                result += variable[i] + '|'
        return result
    
    def return_variable(self, variable_name: str) -> str:
        return self.variables[variable_name]

    def expect_yalex_var(self, line: str) -> str:
        keep_reading = True
        index_to_read = 0
        yalex_var = []
        var_name = ''
        convert = True
        is_group = False
        reading_token = False
        while keep_reading:
            # if var_name in self.variables and not reading_token:
            #     yalex_var.extend(self.variables[var_name])
            #     var_name = ''
            #     index_to_read += len(var_name)
            #     convert = False
            if index_to_read >= len(line) or line[index_to_read] in [LINE_CLOSING]:
                keep_reading = False
            elif line[index_to_read] == ']':
                is_group = False
                index_to_read += 1
                yalex_var.append(self.operators.agrupation[1])
            elif line[index_to_read] == '[':
                is_group = True
                index_to_read += 1
                yalex_var.append(self.operators.agrupation[0])
            elif line[index_to_read] == '"':
                string, move = self.expect_double_quote(line[index_to_read:])
                yalex_var += string
                index_to_read += move + 1
            elif line[index_to_read] == "'":
                string, move = self.expect_single_quote(line[index_to_read:])
                yalex_var.append(string)
                index_to_read += move + 1
            elif line[index_to_read] == '-':
                string, move = self.expect_range(line[index_to_read:], yalex_var[-1])
                yalex_var.pop()
                yalex_var.extend(string)
                index_to_read += move + 1
            elif self.operators.is_agrupation(line[index_to_read]):
                var_name_move = 0
                if reading_token:
                    yalex_var.append(self.return_variable(var_name))
                    var_name = ''
                    var_name_move += len(var_name)
                    convert = False
                yalex_var.append(line[index_to_read])
                index_to_read += 1 + var_name_move
                reading_token = False
            elif self.operators.is_operator(line[index_to_read]):
                var_name_move = 0
                if reading_token:
                    yalex_var.append(self.return_variable(var_name))
                    var_name = ''
                    var_name_move += len(var_name)
                    convert = False
                yalex_var.append(line[index_to_read])
                reading_token = False
                index_to_read += 1 + var_name_move
            else:
                # # if is the firs index then add the letter before
                # if index_to_read == 1:
                #     var_name += line[index_to_read - 1]
                var_name += line[index_to_read]
                index_to_read += 1
                reading_token = True
                # index_to_read += 1
                # else:
                #     yalex_var += line[index_to_read]
                #     index_to_read += 1
        return yalex_var, index_to_read, convert

    def expect_range(self, line:str, start_range: str) -> str:
        range_var = []
        end_range, move = self.expect_single_quote(line[1:])
        range_var.extend(chr(i) for i in range(ord(start_range), ord(end_range) + 1))
        return range_var, 1 + move

    def expect_single_quote(self, line:str) -> str:
        regular_char = line[1]
        if regular_char == '\\':
            regular_char += line[2]
        return regular_char, len(regular_char) + 1
        # keep_reading = True
        # index_to_read = 1
        # regular_char = ''
        # while keep_reading:
        #     if line[index_to_read] == "'":
        #         keep_reading = False
        #     else:
        #         regular_char += line[index_to_read]
        #         index_to_read += 1
        # return regular_char, index_to_read
    
        # regular_char = line[1]
        # return regular_char, len(regular_char) + 1

    def expect_double_quote(self, line:str) -> str:
        keep_reading = True
        index_to_read = 1
        # string_character = ''
        string_character = []
        while keep_reading:
            if line[index_to_read] == '"':
                keep_reading = False
            else:
                # char, move = self.expect_single_quote(f"'{line[index_to_read:]}")
                # string_character += char
                # index_to_read += move
                string_character.append(line[index_to_read])
                index_to_read += 1
        return string_character, index_to_read