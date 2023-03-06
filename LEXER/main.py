'''
  Author: Raul Angel Jimenez
  Main class to run the program
'''
from Controller import Controller
from Menu.Menu import Menu
from time import sleep
# from simple_term_menu import TerminalMenu


def main():
    exit_app = False
    menu = Menu()
    while not exit_app:
        _, option = menu.get_menu(0)
        if option == 0:
            expression = input("Enter a regular expression: ")
            print(f"You entered: {expression}")
            first_option = 0
            while first_option != 2:
                _, first_option = menu.get_menu(1)                
                if first_option == 0:
                    print("Convert regex to NFA (Thompson)")
                    controller = Controller()
                    postfix = controller.convert_infix_to_postfix(expression)
                    if postfix is not None:
                        infix = controller.parser.infix
                        print(f"Infix: {infix}")
                        print(f"Postfix: {postfix}")
                        controller.create_automata(postfix)
                        second_option = 0
                        while second_option != 3:
                            _, second_option = menu.get_menu(2)
                            if second_option == 0:
                                print("Render NFA graph")
                                controller.render_graph()
                            elif second_option == 1:
                                print("Convert NFA to DFA (subsets)")
                                controller.get_dfa_subsets()
                            elif second_option == 2:
                                print("Simulate NFA")
                                input_string = input("Enter a string to simulate: ")
                                print(f"You entered: {input_string}")
                                result = controller.simulate_nfa(input_string)
                                print(f"Result: {result}")
                            elif second_option == 3:
                                print("Back")                        
                elif first_option == 1:
                    print("Convert regex to DFA")
                elif first_option == 2:
                    print("Back")
        elif option == 1:
            # print('===============\nRun tests\n===============\n')
            # controller = Controller()
            # controller.run_tests()
            pass # TODO: Run tests
        elif option == 2:
            print("Bye!")
            exit_app = True
        sleep(2)


if __name__ == "__main__":
    main()
