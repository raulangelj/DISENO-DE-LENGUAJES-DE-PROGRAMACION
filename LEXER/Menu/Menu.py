from pick import pick
from typing import Tuple


class Menu():
    def __init__(self) -> Tuple[str, int]:
        self.option: int = 0
        self.option_value: str = ''

    def get_menu(self, menu: int) -> Tuple[int, str]:
        if menu == 0:
            self.option, self.option_value = self.print_main_menu()
        elif menu == 1:
            self.option, self.option_value = self.print_regex_menu()
        elif menu == 2:
            self.option, self.option_value = self.print_NFA_menu()
        elif menu == 3:
            self.option, self.option_value = self.print_adf_menu()
        return self.option, self.option_value
    
    def print_adf_menu(self):
        title = 'Please choose action to do: '
        options = ['Render DFA graph', 'Minimizar', 'Simulate DFA', 'Back']
        return pick(
            options,
            title,
            multiselect=False,
            default_index=0,
            min_selection_count=1,
            indicator='->',
        )

    def print_main_menu(self):
        title = 'Please choose action to do: '
        options = ['Enter a new regex expression', 'Run tests', 'Exit']
        return pick(
            options,
            title,
            multiselect=False,
            default_index=0,
            min_selection_count=1,
            indicator='->',
        )

    def print_regex_menu(self):
        title = 'Please choose action to do: '
        options = [
            'Convert regex to NFA (Thompson)', 'Convert regex to DFA', 'Back']
        return pick(
            options,
            title,
            multiselect=False,
            default_index=0,
            min_selection_count=1,
            indicator='->',
        )

    def print_NFA_menu(self):
        title = 'Please choose action to do: '
        options = ['Render NFA graph', 'Convert NFA to DFA (subsets)', 'Simulate NFA', 'Back']
        return pick(
            options,
            title,
            multiselect=False,
            default_index=0,
            min_selection_count=1,
            indicator='->',
        )
