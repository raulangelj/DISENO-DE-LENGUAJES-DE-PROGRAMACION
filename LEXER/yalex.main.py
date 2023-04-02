from YALEX.YALEX import Yalex
from termcolor import colored
from Convertor.ConvertorAlgorithms import Algorithms
from Tree.Tree import Tree


def main():
    running = True
    while running:
        print('''
        1. Leer archivo\n
        2. Salir\n''')
        option = input('Ingrese una opción: ')
        if option == '1':
            try:
                file_path = input('Ingrese la ruta del archivo: ')
                algorithms = Algorithms()
                yalex = Yalex(file_path)
                yalex.read_file()
                postfix = algorithms.get_result_postfix(yalex.expression)
                tree = Tree(postfix=postfix)
                tree.create_tree()
                tree.render_tree(tree.tree)
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
