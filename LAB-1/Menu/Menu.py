from pick import pick
from typing import Tuple

class Menu():
	def __init__(self) -> Tuple[str, int]:
		self.option: int = 0
		self.option_value: str = ''

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