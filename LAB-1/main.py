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
            print('===============\nConvert from infix to postfix\nTo exit enter "exit"\n===============\n')
            expression = input("Enter a regular expression: ")
            while expression != "exit":
                print(f"You entered: {expression}")
                convertor = Convertor()
                postfix = convertor.convert_from_infix_to_postfix(expression)
                if postfix is not None:
                    print(f"Postfix: {postfix}")
                expression = input("\nEnter a regular expression: ").lower()
        elif option.lower() in ["2", "exit"]:
            print("Bye!")
            exit_app = True


if __name__ == "__main__":
    main()
