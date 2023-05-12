from __future__ import annotations

class TokenSintactic():
    def __init__(self, value: str) -> None:
        self.value = value

    def __eq__(self, __value: TokenSintactic) -> bool:
        return self.value == __value.value