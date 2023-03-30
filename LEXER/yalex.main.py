from YALEX.YALEX import Yalex

def main():
    yalex = Yalex('LEXER/Mocks/YALEX/slr-test.yal')
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



if __name__ == "__main__":
    main()
