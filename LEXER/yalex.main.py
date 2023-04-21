import os
import glob
import pickle
from src.YALEX.YALEX import Yalex
from termcolor import colored
from Convertor.ConvertorAlgorithms import Algorithms
from Convertor.Parser import Parser
from Tree.Tree import Tree
from Automata.DFA import DFA
from Convertor.Character import *

RUTE_COMPILER = 'LEXER/'

compiler_content = '''from Automata.DFA import DFA
from Convertor.Character import *
import os
import pickle

def main():
    file_path = input('Ingrese la ruta del archivo: ')
    file_data = ''
    with open(file_path, 'r') as file:
        for line in file:
            for character in line:
                file_data += character
    tokens = None
    with open('LEXER/automata.pkl', 'rb') as file:
        automata = pickle.load(file)
        sentence = Characters(file_data)
        tokens = automata.simulate(sentence)
    for token in tokens:
        if token.token_type.value != 1:
            return_val = token.accepted_state.return_value.value[1:-1].strip() if token.accepted_state.return_value else ''
            exec(return_val)
        else:
            print(f'TOKEN NO VALIDO: {token.characters}')
if __name__ == '__main__':
    main()
'''

def create_scanner():
    # # create the deps files
    # directories = ['LEXER/Automata', 'LEXER/Convertor', 'LEXER/Tree', 'LEXER/YALEX']
    # # directories = ['LEXER/Tree', 'LEXER/YALEX']
    # py_files = []
    # for directory in directories:
    #     py_files += glob.glob(os.path.join(directory, '*.py'))
    # # create the vendor.py
    # new_file = 'vendor.py'
    # with open(f'{RUTE_COMPILER}{new_file}', 'w') as f:
    #     # iterate over each .py file
    #     for py_file in py_files:
    #         with open(py_file, 'r') as g:
    #             # read the contents of the .py file
    #             contents = g.readlines()
    #             # write the contents to the new file, skipping any import lines
    #             for line in contents:
    #                 if 'import' not in line or 'typing' in line:
    #                     f.write(line)
    #         f.write('\n')
    # create another file name as scanner.py in which when run it will ask the user for a file path to open that file and print all the characters in the file
    # create the directory if it does not exist
    if not os.path.exists(RUTE_COMPILER):
        os.makedirs(RUTE_COMPILER)
    with open(f'{RUTE_COMPILER}scanner.py', 'w') as file:
        file.write(compiler_content)
    # run the file created
    # os.system(f'python {RUTE_COMPILER}scanner.py')

def main():
    running = True
    while running:
        print('''
        1. Leer archivo\n
        2. Salir\n''')
        option = input('Ingrese una opción: ')
        if option == '1':
            try:
                # file_path = input('Ingrese la ruta del archivo: ')
                file_path = 'LEXER/Mocks/YALEX/slr-4.yal'
                algorithms = Algorithms()
                yalex = Yalex(file_path)
                yalex.read_file()
                postfix = algorithms.get_result_postfix(yalex.expression)
                tree = Tree(postfix=postfix)
                tree.create_tree()
                tree.render_tree(tree.tree)
                parser = Parser()
                clean_infix = parser.remove_special_characters(yalex.expression)
                new_postfix = algorithms.get_result_postfix(clean_infix)
                tree_automata = Tree(new_postfix, yalex.rules)
                tree_automata.create_tree()
                tree_automata.render_tree(tree_automata.tree)
                tree_automata.followpos_recursive(tree_automata.tree)
                adf = DFA()
                adf.create_automata(postfix=new_postfix, tree=tree_automata, infix=clean_infix, originial=clean_infix)
                adf.create_graph('DFA')
                # print(adf.simulate('hola'))
                # print(adf.simulate(' '))
                # print(adf.simulate('1'))
                # print(adf.simulate(';'))
                # print(adf.simulate(')'))
                # print(adf.simulate('11.11E-11'))
                # print(adf.simulate('1.1.1.E15'))
                # create a pickle file with the automata
                with open(f'{RUTE_COMPILER}automata.pkl', 'wb') as file:
                    pickle.dump(adf, file)

                create_scanner()
                # text_to_analyze = ''
                # # open file cualquiera.txt that is in the same folder as this file
                # with open('LEXER/cualquiera.txt', 'r') as file:
                #     for line in file:
                #         for character in line:
                #             text_to_analyze += character
                # sentece = Characters(text_to_analyze)
                # print(adf.simulate(sentece))
                            # tree.followpos_recursive(tree.tree)
                            # dfa = DFA()
                            # dfa.create_automata(postfix=postfix, tree=tree, infix=yalex.expression, originial=yalex.expression)
                            # dfa.create_graph('DFA')
            except Exception as e:
                print(colored(e, 'red'))
        elif option == '2':
            running = False
            print('Adios')
        else:
            print('Ingrese una opción válida')

    # yalex = Yalex('LEXER/Mocks/YALEX/slr-1.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-2.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-3.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-4.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-test.yal')
    # algorithms = Algorithms()
    # print(yalex.expect_single_quote("'\n'"))
    # print(yalex.expect_single_quote("'a'"))
    # print(yalex.expect_double_quote('"\t\n "'))
    # print(yalex.expect_double_quote('"bbbb"'))
    # print(yalex.expect_yalex_var("['a']"))
    # print(yalex.expect_yalex_var("['a''b''c']"))
    # print(yalex.expect_yalex_var('["def"]'))
    # print(yalex.expect_yalex_var("['a'-'z']"))
    # print(yalex.expect_yalex_var("['A'-'Z''a'-'z']"))
    # print(yalex.varaible_declaration("let letter = ['A'-'Z''a'-'z']"))
    # try:
    #     yalex.read_file()
    #     postfix = algorithms.get_result_postfix(yalex.expression)
    #     # print('postfix')
    #     # print(postfix)
    #     tree = Tree(postfix=postfix)
    #     tree.create_tree()
    #     tree.render_tree(tree.tree)
    # except Exception as e:
    #     print(colored(e, 'red'))
    # print('termino')


if __name__ == "__main__":
    main()
