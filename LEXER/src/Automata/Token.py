from __future__ import annotations
from typing import TypedDict, List


class TokenModel():
    value: str
    ascii: int


class Token():
    def __init__(self, value, label=None):
        self.value = value
        # self.ascii = chr(int(value))
        self.label = label

    def model(self) -> TokenModel:
        return {
            'value': self.value,
            'ascii': self.ascii
        }

    def __str__(self) -> str:
        return f'value: {self.value}, ascii: {self.ascii}'

    def is_in(self, tokens: List[Token]) -> bool:
        return any(token.value == self.value for token in tokens)

    def print_token(self) -> None:
        print("+--------------------+----------+")
        print("| Token              | Value    |")
        print("+--------------------+----------+")
        print("|{:<20}|{:>10}|".format('Value', self.value))
        print("|{:<20}|{:>10}|".format('Ascii', self.ascii))
        print("+--------------------+----------+")
