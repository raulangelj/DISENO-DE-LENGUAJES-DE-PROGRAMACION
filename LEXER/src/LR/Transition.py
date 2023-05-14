from src.LR.StateSintactic import StateSintactic
from src.LR.TokenSintactic import TokenSintactic

class Transition():
    def __init__(self, origin: StateSintactic, destination: StateSintactic, simbol:TokenSintactic) -> None:
        self.origin: StateSintactic = origin
        self.destination: StateSintactic = destination
        self.simbol: TokenSintactic = simbol