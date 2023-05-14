from __future__ import annotations
from typing import List
from src.LR.Production import Production

class StateSintactic():
    def __init__(self) -> None:
        self.id: str = ''
        self.items: List[Production] = []
        self.clousure: List[Production] = []

    def state_label(self) -> str:
        items = "".join([f' {str(p)} \\l ' for p in self.items])
        # clousure = "".join([f' {str(p)} \\l ' for p in self.clousure])
        # add in clousure the str(p) if the str is not in items
        clousure = "".join([f' {str(p)} \\l ' for p in self.clousure if str(p) not in items])
        return f'{"{"}{self.id} | {items} | {clousure}{"}"}'
    
    def __eq__(self, __value: StateSintactic) -> bool:
        # check if the items are the same
        if len(self.items) != len(__value.items):
            return False
        for i in range(len(self.items)):
            if self.items[i] != __value.items[i]:
                return False
        # check if the clousure are the same
        if len(self.clousure) != len(__value.clousure):
            return False
        return all(
            self.clousure[i] == __value.clousure[i]
            for i in range(len(self.clousure))
        )