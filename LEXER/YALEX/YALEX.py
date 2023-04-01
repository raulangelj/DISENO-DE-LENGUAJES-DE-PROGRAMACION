from typing import List
from Convertor.Simbols import Operators

LINE_CLOSING = '\n'


class Yalex():
    def __init__(self, file_to_read: str) -> None:
        self.file_to_read = file_to_read
        self.variables = {}
        self.operators = Operators()
        self.rule = ''
        self.expression = ''

    def read_file(self) -> None:
        filex_text = ''
        with open(self.file_to_read, 'r') as file:
            # TODO: quitar breaks y hacerlo con index y las funciones me van a regresar cuantos me movi
            for line in file:
                for char in line:
                    filex_text += char
                    # word += char
                    # if word == 'rule ' or reading_rule:
                    #     rule_text += char
                    #     reading_rule = True
                    #     if rule_text[-1] == LINE_CLOSING and rule_text[-2] == LINE_CLOSING:
                    #         reading_rule = False
                    #         self.rule_declaration(rule_text[1:])
                    #         rule_text = ''
                    #         break
                    # elif word == 'let ':
                    #     self.variable_declaration(line[4:]) # 4 because we already read the 'let ' word
                    #     word = ''
                    #     break
        keep_reading = True
        word = ''
        index = 0
        reading_rule = False
        rule_text = ''
        while keep_reading:
            if index > len(filex_text) - 1:
                keep_reading = False
            elif filex_text[index] != LINE_CLOSING:
                word += filex_text[index]
                if word == 'rule ' or reading_rule:
                    index += 1 # add 1 because we already read the ' ' word
                    move = self.rule_declaration(filex_text[index:])
                    index += move
                    word = ''
                    # rule_text += filex_text[index]
                    # reading_rule = True
                    # if rule_text[-1] == LINE_CLOSING and rule_text[-2] == LINE_CLOSING:
                    #     reading_rule = False
                    #     move = self.rule_declaration(rule_text[1:])
                    #     index += move
                    #     rule_text = ''
                elif word == 'let ':
                    # 4 because we already read the 'let ' word
                    index += 1 # add 1 because we already read the ' ' word
                    move = self.variable_declaration(filex_text[index:])
                    index += move
                    word = ''
            index += 1

        self.expression = self.operators.concat.validate(self.rule)
        return self.expression

    def rule_declaration(self, line: str) -> None:
        keep_reading = True
        # index_to_read = 5 # 5 because we already read the 'rule ' word
        index_to_read = 0
        # find the rule name
        rule_name = ''
        var_name = ''
        while keep_reading:
            if line[index_to_read] == ' ':
                keep_reading = False
            else:
                rule_name += line[index_to_read]
                index_to_read += 1
        # find the rule value
        keep_reading = True
        index_to_read += 2  # 2 because we already read the '= ' word
        rule_value = {}
        rule_returns = {}
        reading_return = False
        while keep_reading:
            if index_to_read >= len(line):
                keep_reading = False
            elif line[index_to_read] == '}':
                reading_return = False
            elif line[index_to_read] == '{' or reading_return:
                reading_return = True
            elif (
                line[index_to_read] is not LINE_CLOSING
                and line[index_to_read] != ' '
                and not self.operators.is_operator(line[index_to_read])
                and line[index_to_read] != "'"
            ):
                var_name += line[index_to_read]
            elif line[index_to_read] == "'":
                string, move = self.expect_single_quote(line[index_to_read:])
                var_name += string
                index_to_read += move
                rule_value[var_name] = var_name
                # arreglar para que lea loq ue viene
                rule_returns[var_name] = var_name
                var_name = ''
            elif var_name != ' ' and var_name in self.variables:
                rule_value[var_name] = self.variables[var_name]
                # arreglar para que lea loq ue viene
                rule_returns[var_name] = var_name
                var_name = ''
            index_to_read += 1
        rule_value_string = '('
        for value in rule_value.values():
            rule_value_string += f'({value})|'
        rule_value_string = f'{rule_value_string[:-1]})'
        self.rule = rule_value_string
        return index_to_read

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
        index_to_read += 3 # 3 because we already read the ' = ' word
        yalex_var, move, convert = self.expect_yalex_var(
            line[index_to_read:])
        index_to_read += move
        self.variables[variable_name] = self.convert_to_expression(
            yalex_var) if convert else "".join(yalex_var)
        return index_to_read
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
                string, move = self.expect_range(
                    line[index_to_read:], yalex_var[-1])
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

    def expect_range(self, line: str, start_range: str) -> str:
        range_var = []
        end_range, move = self.expect_single_quote(line[1:])
        range_var.extend(str(i).zfill(3)
                         for i in range(int(start_range), int(end_range) + 1))
        return range_var, 1 + move

    def expect_single_quote(self, line: str) -> str:
        ascii_char = str(ord(line[1])).zfill(3)
        regular_char = line[1]
        if regular_char == '\\':
            regular_char += line[2]
            ascii_char += str(ord(line[2])).zfill(3)
        # ascii_char = str(ord(regular_char[0])).zfill(3) + str(ord(regular_char[1])).zfill(3)
        return ascii_char, len(regular_char) + 1
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

    def expect_double_quote(self, line: str) -> str:
        keep_reading = True
        index_to_read = 1
        # string_character = ''
        string_character = []
        ascii_char = []
        while keep_reading:
            if line[index_to_read] == '"':
                keep_reading = False
            else:
                # char, move = self.expect_single_quote(f"'{line[index_to_read:]}")
                # string_character += char
                # index_to_read += move
                string_character.append(line[index_to_read])
                ascii_char.append(str(ord(line[index_to_read])).zfill(3))
                index_to_read += 1
        return string_character, index_to_read
