'''
  Author: Raul Angel Jimenez
  Main class to run the program
'''
from Controller import Controller
from Menu.Menu import Menu
from time import sleep
# from Automata.NFA import NFA


def main():
    exit_app = False
    while not exit_app:
        _, option = Menu().print_main_menu()
        if option == 0:
            expression = input("Enter a regular expression: ")
            print(f"You entered: {expression}")
            controller = Controller()
            postfix = controller.convert_infix_to_postfix(expression)
            if postfix is not None:
                infix = controller.parser.infix
                print(f"Infix: {infix}")
                print(f"Postfix: {postfix}")
                controller.create_automata(postfix)
                controller.render_graph()
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
