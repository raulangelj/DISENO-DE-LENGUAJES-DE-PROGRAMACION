concat_simbol = '·'
or_simbol = '|'
kleene_simbol = '*'
plus_simbol = '+'
optional_simbol = '?'
empty_simbol = 'ε'

terminal_simbol = '#'

special_operators = [plus_simbol, optional_simbol]
operators = [or_simbol, concat_simbol, kleene_simbol] + special_operators


left_agrupations = ['(']
right_agrupations = [')']
agrupations = left_agrupations + right_agrupations

or_yapar = '┇'

escape_characters = {
    '\\n': ord('\n'),
    '\\r': ord('\r'),
    '\\t': ord('\t'),
    '\\': ord('\\'),
    # '\'': ord('\''),
    '\\"': ord('\"'),
    '\\b': ord('\b'),
    '\\f': ord('\f'),
    '\\v': ord('\v'),
}
