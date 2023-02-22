from Convertor.Operators.Constants import UNION_SIMBOL, KLEENE_SIMBOL, PLUS_SIMBOL, OPTIONAL_SIMBOL
from Convertor.Operators.Operator import Operator
from Automata.Automata import Automata
from Automata.EmptyToken import EmptyToken
from Automata.State import State


class Or(Operator):
	def __init__(self):
		super().__init__()
		self.simbol = UNION_SIMBOL
		self.priority = 1
		self.errors = [
			'Invalid expresion: kleene can\'t be the first simbol or its second operator be a kleene/union/optional/plus.\n',
			'Invalid expresion: missing one operator.'
		]

	'''
		* Validate the expression and return the new expression and the number of positions to move
		@param factors: the expression to validate
		@param index: the index of the simbol to validate
		@param expression: the original expression
		@return: new expression, number of positions to move, if the move was forward true else false
	'''

	def validate(self, factors, index, expression):
		# sourcery skip: raise-specific-error
		caracter_before = factors[-1] if len(factors) > 0 else ''
		caracter_after = expression[index +
									1] if index < len(expression) - 1 else ''
		# TODO: add the plus and optional simbols to this validation
		if len(factors) == 0 or caracter_after in [self.simbol, self.kleene_simbol, self.optional_simbol, self.plus_simbol]:
			# * can't be the first simbol or its second operator be a kleene/union/optional/plus
			raise Exception(self.errors[0])
		elif not caracter_after:
			raise Exception(self.errors[1])
		# [actual , '(', ...]
		elif caracter_after is self.agrupation[0]:
			# agrupation_or, positions_move = self.find_agrupation(
			# 	expression, True, index)
			agrupation_or, positions_move = self.find_agrupation_forward(
				expression, index)
			if KLEENE_SIMBOL or UNION_SIMBOL or PLUS_SIMBOL or OPTIONAL_SIMBOL in agrupation_or:
				return agrupation_or, positions_move, True, caracter_before
			return f'{caracter_before}{self.simbol}{agrupation_or}', positions_move, True
		# [')', actual ...]
		elif caracter_before is self.agrupation[1]:
			agrupation_or, positions_move = self.find_agrupation(
				factors)
			return f'{agrupation_or}{self.simbol}{caracter_after}', positions_move, False
		else:
			return f'{caracter_before}{self.simbol}{caracter_after}', 1, False

	def parse(self, agrupation_or, caracter_before='', caracter_after='', positions_move=1):
		if caracter_before:
			return f'{caracter_before}{self.simbol}{agrupation_or}', positions_move, True

	def get_automata_rule(self, operator1: Automata, operator2: Automata, state_counter: int):
		# New first state
		new_first_state = State(is_initial=True, value=state_counter)
		state_counter += 1
		# New last state
		new_last_state = State(is_final=True, value=state_counter)
		# Remove the old first and last states
		operator1.initial_state.is_initial = False
		operator1.final_state.is_final = False
		operator2.initial_state.is_initial = False
		operator2.final_state.is_final = False
		# Create new automata
		automata = Automata()
		# Add the new states
		automata.states = operator1.states + operator2.states + [new_first_state, new_last_state]
		# Add the alphabet
		automata.add_alphabet(operator1.alphabet + operator2.alphabet + [EmptyToken()])
		# Add the transitions
		automata.transitions.transitions = operator1.transitions.transitions + operator2.transitions.transitions
		# Add the new transitions
		automata.transitions.add_transition(new_first_state, EmptyToken(), operator1.initial_state)
		automata.transitions.add_transition(new_first_state, EmptyToken(), operator2.initial_state)
		automata.transitions.add_transition(operator1.final_state, EmptyToken(), new_last_state)
		automata.transitions.add_transition(operator2.final_state, EmptyToken(), new_last_state)
		# Set the new first and last states
		automata.initial_state = new_first_state
		automata.final_state = new_last_state
		return automata
