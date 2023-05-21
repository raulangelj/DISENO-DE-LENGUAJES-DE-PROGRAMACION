from __future__ import annotations
from typing import List
from src.LR.TokenSintactic import TokenSintactic

class Production():
    def __init__(self, value=None) -> None:
        if value is None:
            value = []
        self.value: List[TokenSintactic] = value

    def add(self, token: TokenSintactic) -> None:
        self.value.append(token)

    def first_token(self) -> TokenSintactic:
        return self.value[0]
    
    # * This method is used to get the first token of the expression
    # * that is after the arrow
    def first_token_expression(self) -> TokenSintactic:
        return self.value[2]
    
    def last_token(self) -> TokenSintactic:
        return self.value[-1]
    
    def index_of(self, token: TokenSintactic) -> int:
        return next(
            (
                i
                for i in range(len(self.value))
                if self.value[i].value == token.value
            ),
            -1,
        )

    def __str__(self) -> str:
        return ' '.join([token.value for token in self.value])
    
    def __eq__(self, __value: Production) -> bool:
        # check if the items are the same
        if len(self.value) != len(__value.value):
            return False
        return all(self.value[i] == __value.value[i] for i in range(len(self.value)))