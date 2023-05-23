from __future__ import annotations
from typing import List
from src.LR.TokenSintactic import TokenSintactic
from src.Tokens.Tokens import dot_ls

class Production():
    def __init__(self, value=None) -> None:
        if value is None:
            value = []
        self.value: List[TokenSintactic] = value
        self.prodduction_: str = str(self)

    def add(self, token: TokenSintactic) -> None:
        self.value.append(token)
    
    def has_final_dot(self) -> bool:
        return self.value[-1].value == dot_ls

    def first_token(self) -> TokenSintactic:
        return self.value[0]
    
    def next_token(self, token: TokenSintactic) -> TokenSintactic or None:
        index = self.index_of(token)
        index = index + 1 if index != -1 and index + 1 < len(self.value) else -1
        return self.value[index] if index != -1 else None
    
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
                for i in range(1, len(self.value))
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
    
    def __contains__(self, __value: TokenSintactic) -> bool:
        return any(exp.value == __value.value for exp in self.value[2:])