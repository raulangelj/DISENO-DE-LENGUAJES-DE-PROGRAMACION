from YALEX.YALEX import Yalex
from Convertor.ConvertorAlgorithms import Algorithms
from Tree.Tree import Tree

def main():
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-test.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-1.yal')
    yalex = Yalex('LEXER/Mocks/YALEX/slr-2.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-1.yal')
    # yalex = Yalex('LEXER/Mocks/YALEX/slr-1.yal')
    algorithms = Algorithms()
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
    print(yalex.read_file())
    postfix = algorithms.get_result_postfix(yalex.expression)
    tree = Tree(postfix= postfix)
    tree.create_tree()
    tree.render_tree(tree.tree)
    print('termino')




if __name__ == "__main__":
    main()
