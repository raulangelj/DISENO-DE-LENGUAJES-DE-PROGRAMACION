from enum import Enum

'''Types of characters: 'SIMBOL', 'OPERATOR', 'AGRUPATION' '''

# character_types = {
#     'SIMBOL': 'SIMBOL',
#     'OPERATOR': 'OPERATOR',
#     'AGRUPATION': 'AGRUPATION',
# }

class character_types():
    SIMBOL = 'SIMBOL'
    OPERATOR = 'OPERATOR'
    AGRUPATION = 'AGRUPATION'
    FINAL = 'FINAL'
    EMPTY = 'EMPTY'

character_types = Enum('character_types', ['SIMBOL', 'OPERATOR', 'AGRUPATION', 'FINAL', 'EMPTY'])

class Character():
    def __init__(self, value: str = None, type: str = 'SIMBOL', label: str = None) -> None:
        self.value = value
        self.type = type
        self.label = label or value 