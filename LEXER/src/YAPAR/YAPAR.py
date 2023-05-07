
from src.Tokens.Tokens import *
from src.Automata.DFA import DFA, tokenListModel
from src.Convertor.Parser import Parser
from src.Convertor.ConvertorAlgorithms import Algorithms
from src.Tree.Tree import Tree
from src.Convertor.Character import *


ID_INFIX = f'(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z){concat_simbol}((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*'

TOKEN_INFIX = f'%{concat_simbol}t{concat_simbol}o{concat_simbol}k{concat_simbol}e{concat_simbol}n{concat_simbol}( {concat_simbol}{ID_INFIX})+{concat_simbol}#'

# EXPRESION_INFIX = f':{concat_simbol}\\n{concat_simbol}#'
EXPRESION_INFIX = f'{ID_INFIX}{concat_simbol}:{concat_simbol}\\n{concat_simbol}( {concat_simbol} *){concat_simbol}{ID_INFIX}{concat_simbol}( {concat_simbol}{ID_INFIX})*{concat_simbol}\\n{concat_simbol}( +{concat_simbol}{or_yapar}{concat_simbol}( {concat_simbol}{ID_INFIX})+{concat_simbol}\\n)*{concat_simbol};{concat_simbol}#'

class Token_data:
    def __init__(self) -> None:
        self.token_infix: Characters = None
        self.token_postfix: Characters = None
        self.token_tree: Tree = None
        self.token_dfa: DFA = None
        self.token_ids: List[Characters] = None

class Expression_data:
    def __init__(self) -> None:
        self.expression_infix: Characters = None
        self.expression_postfix: Characters = None
        self.expression_tree: Tree = None
        self.expression_dfa: DFA = None
        self.expression_ids: List[Characters] = None


class Yapar():
    def __init__(self) -> None:
        self.token_data = Token_data()
        self.expression_data = Expression_data()
        self.generate_token_dfa()
        self.generate_expression_dfa()

    def change_operators_chars(self, chars: Characters) -> Characters:
        # convert the |, concat y kleene to operators and the (,) to agrupations
        for token in chars.characters:
            if token.label in operators:
                token.value = token.label
                token.type = character_types.OPERATOR
            elif token.label == terminal_simbol:
                token.value = token.label
                token.type = character_types.FINAL
            elif token.label in agrupations:
                token.value = token.label
                token.type = character_types.AGRUPATION
            elif token.label in escape_characters:
                token.value = str(escape_characters[token.label]).zfill(3)
                token.type = character_types.SPECIAL_CHAR
        return chars

    def generate_expression_dfa(self) -> None:
        expresion_dfa = DFA()
        expresion_c = Characters(characters=EXPRESION_INFIX)
        expresion_c = self.change_operators_chars(expresion_c)
        expresion_c.change_char(or_yapar, or_simbol)
        expresion_i = Parser().remove_special_characters(expresion_c.characters)
        expresion_i = Characters(characters_list=expresion_i)
        expresion_p = Algorithms().get_result_postfix(expresion_i.characters)
        expresion_p = Characters(characters_list=expresion_p)
        expresion_t = Tree(postfix=expresion_p.characters)
        expresion_t.create_tree()
        expresion_t.followpos_recursive(expresion_t.tree)
        expresion_dfa.create_automata(
            postfix=expresion_p, tree=expresion_t, infix=expresion_i.characters, originial=expresion_i)
        # test = Characters(characters='m:\\n  a\\n;')
        # test1 = Characters(characters='m:\\n  a SEMICOLON m q\\n;')
        # test2 = Characters(characters='q:\\n    SEMICOLON m q\\n  | SEMICOLON m\\n;')
        # expresion_dfa.simulate(test2)
        # print('termino')
        # get all the expresions
        self.expression_data.expression_infix = expresion_i
        self.expression_data.expression_postfix = expresion_p
        self.expression_data.expression_tree = expresion_t
        self.expression_data.expression_dfa = expresion_dfa
        del expresion_dfa, expresion_c, expresion_i, expresion_p, expresion_t

    def generate_token_dfa(self) -> None:
        parser = Parser()
        algorithms = Algorithms()
        token_dfa = DFA()
        token_c = Characters(characters=TOKEN_INFIX)
        token_c = self.change_operators_chars(token_c)
        token_i = parser.remove_special_characters(token_c.characters)
        token_i = Characters(characters_list=token_i)
        token_p = algorithms.get_result_postfix(token_i.characters)
        token_p = Characters(characters_list=token_p)
        token_t = Tree(postfix=token_p.characters)
        token_t.create_tree()
        token_t.followpos_recursive(token_t.tree)
        token_dfa.create_automata(
            postfix=token_p, tree=token_t, infix=token_i.characters, originial=token_i)
        # test = Characters(characters='%token TIMES')
        # token_dfa.simulate(test)
        # print('termino')
        # get all the tokens
        self.token_data.token_infix = token_i
        self.token_data.token_postfix = token_p
        self.token_data.token_tree = token_t
        self.token_data.token_dfa = token_dfa
        del parser
        del algorithms
        del token_c
        del token_i
        del token_p
        del token_t
        del token_dfa

    def read_file(self, file_name: str) -> List[tokenListModel]:
        file_text = ''
        with open(file_name, 'r') as file:
            for line in file:
                for char in line:
                    file_text += char
        # get tokens
        tokens = self.token_data.token_dfa.simulate(
            Characters(characters=file_text))
        tokens = self.clean_tokens(tokens)
        self.token_data.token_ids = tokens
        # get expresions
        expresions = self.expression_data.expression_dfa.simulate(
            Characters(characters=file_text))
        expresions = self.clean_expressions(expresions)
        self.expression_data.expression_ids = expresions
        self.print_data()

    def get_terminal(self, exp: Characters) -> Characters:
        terminal = f'{ID_INFIX}{concat_simbol}:{concat_simbol}#'
        terminal_c = Characters(characters=terminal)
        terminal_c = self.change_operators_chars(terminal_c)
        terminal_i = Parser().remove_special_characters(terminal_c.characters)
        terminal_i = Characters(characters_list=terminal_i)
        terminal_p = Algorithms().get_result_postfix(terminal_i.characters)
        terminal_p = Characters(characters_list=terminal_p)
        terminal_t = Tree(postfix=terminal_p.characters)
        terminal_t.create_tree()
        terminal_t.followpos_recursive(terminal_t.tree)
        terminal_dfa = DFA()
        terminal_dfa.create_automata(
            postfix=terminal_p, tree=terminal_t, infix=terminal_i.characters, originial=terminal_i)
        terminal = terminal_dfa.simulate(exp)
        return terminal[0].characters


    def clean_expressions(self, expresions: List[tokenListModel]) -> List[Characters]:
        expressions = []
        for e in expresions:
            chars = e.characters
            terminal = self.get_terminal(chars)
            # print(terminal)
            # find all the expressions separated by |
            exp_c = f'({ID_INFIX}{concat_simbol}( )?)+{concat_simbol}{terminal_simbol}'
            exp_c = Characters(characters=exp_c)
            exp_c = self.change_operators_chars(exp_c)
            exp_i = Parser().remove_special_characters(exp_c.characters)
            exp_i = Characters(characters_list=exp_i)
            exp_p = Algorithms().get_result_postfix(exp_i.characters)
            exp_p = Characters(characters_list=exp_p)
            exp_t = Tree(postfix=exp_p.characters)
            exp_t.create_tree()
            exp_t.followpos_recursive(exp_t.tree)
            exp_dfa = DFA()
            exp_dfa.create_automata(
                postfix=exp_p, tree=exp_t, infix=exp_i.characters, originial=exp_i)
            expression_input = str(chars)
            expression_input = expression_input[len(str(terminal)):].strip()
            exp = exp_dfa.simulate(Characters(characters=expression_input))
            for a in exp:
                real_expression = Characters()
                real_expression.characters = terminal.characters + a.characters.characters
                expressions.append(real_expression)
        return expressions


    def clean_tokens(self, tokens: List[tokenListModel]) -> List[Characters]:
        tokens_string = ''
        for token in tokens:
            token_id = str(token.characters)[7:]
            tokens_string += f'{token_id} '
        # create a id dfa to simulate the tokens and get only the tokens id
        id_c = Characters(characters=f'{ID_INFIX}{concat_simbol}#')
        id_c = self.change_operators_chars(id_c)
        id_i = Parser().remove_special_characters(id_c.characters)
        id_i = Characters(characters_list=id_i)
        id_p = Algorithms().get_result_postfix(id_i.characters)
        id_p = Characters(characters_list=id_p)
        id_t = Tree(postfix=id_p.characters)
        id_t.create_tree()
        id_t.followpos_recursive(id_t.tree)
        id_dfa = DFA()
        id_dfa.create_automata(postfix=id_p, tree=id_t,
                               infix=id_i, originial=id_i)
        # simulate the tokens
        tokens = id_dfa.simulate(Characters(characters=tokens_string))
        return [token.characters for token in tokens]

    def print_data(self) -> None:
        print('Tokens: ')
        for token in self.token_data.token_ids:
            print(token)
        print('Expresions: ')
        for exp in self.expression_data.expression_ids:
            print(exp)
        