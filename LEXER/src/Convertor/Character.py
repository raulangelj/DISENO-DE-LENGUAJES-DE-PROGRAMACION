from src.Tokens.Tokens import *
from typing import List
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
    SPECIAL_CHAR = 'SPECIAL_CHAR'


character_types = Enum('character_types', [
                       'SIMBOL', 'OPERATOR', 'AGRUPATION', 'FINAL', 'EMPTY', 'SPECIAL_CHAR'])


class Character():
    def __init__(self, value: str = None, type: str = 'SIMBOL', label: str = None) -> None:
        self.value = value
        self.type = type
        self.label = label or value


class Characters():
    def __init__(self, characters: List[str] = None, characters_list: List[Character] = None) -> None:
        if characters is None:
            characters = []
        self.characters = self.convert_to_characters(characters)
        if characters_list is not None:
            self.characters = characters_list
        self.word = self.__str__()

    def convert_to_characters(self, value: str) -> List[Character]:
        characters = []
        index = 0
        while index < len(value):
            character = value[index]
            ascii_val = str(ord(character)).zfill(3)
            if character == '\\':
                index += 1
                character += value[index]
                ascii_val = str(escape_characters[character]).zfill(3)
            characters.append(
                Character(value=ascii_val, type=character_types.SIMBOL, label=character))
            index += 1
        return characters
    
    def change_char(self, char: str, new_char: str) -> None:
        for character in self.characters:
            if character.label == char:
                character.label = new_char
                character.value = str(ord(new_char)).zfill(3)

    def __str__(self) -> str:
        return "".join([character.label for character in self.characters])
