class TokenSintactic():
    def __init__(self, value: str) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value