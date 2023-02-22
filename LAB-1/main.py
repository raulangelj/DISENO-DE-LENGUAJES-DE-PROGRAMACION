'''
  Author: Raul Angel Jimenez
  Main class to run the program
'''
from Menu.Menu import initial_menu
from Controller import Controller
# from Automata.NFA import NFA


def main():
    exit_app = False
    while not exit_app:
        print(initial_menu)
        option = input("Select an option: ")
        if option == "1":
            print('===============\nConvert from infix to postfix\nTo exit enter "exit"\n===============\n')
            expression = input("Enter a regular expression: ")
            while expression != "exit":
                print(f"You entered: {expression}")
                controller = Controller()
                postfix = controller.convert_infix_to_postfix(expression)
                if postfix is not None:
                    infix = controller.parser.infix
                    print(f"Infix: {infix}")
                    print(f"Postfix: {postfix}")
                    controller.create_automata(postfix)
                    # create_graph = input("Do you want to create a graph? (y/N): ")
                    # if create_graph.lower() == "y":
                    #     file_name = input("Enter the file name or path for the graph: ")
                    #     controller.render_graph(file_name)
                    controller.render_graph()
                expression = input("\nEnter a regular expression: ").lower()
        elif option.lower() in ["2", "exit"]:
            print("Bye!")
            exit_app = True


if __name__ == "__main__":
    main()
