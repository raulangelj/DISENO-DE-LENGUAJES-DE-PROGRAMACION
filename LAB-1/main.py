'''
  Author: Raul Angel Jimenez
  Main class to run the program
'''
from Menu.Menu import initial_menu
from Convertor.Convertor import Convertor


def main():
    exit_app = False
    while not exit_app:
        print(initial_menu)
        option = input("Select an option: ")
        if option == "1":
            expression = input("Enter a regular expression: ")
            print(f"You entered: {expression}")
            convertor = Convertor()
            postfix = convertor.convert_from_infix_to_postfix(expression)
            print(f"Postfix: {postfix}")

        elif option == "2":
            print("Bye!")
            exit_app = True


if __name__ == "__main__":
    main()
