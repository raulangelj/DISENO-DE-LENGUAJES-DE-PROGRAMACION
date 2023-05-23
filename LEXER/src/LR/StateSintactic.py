from __future__ import annotations
from typing import List
from enum import Enum
from src.LR.Production import Production


state_types = Enum('state_types', [
                       'record', 'plain'])

class StateSintactic():
    def __init__(self, type: state_types = state_types.record) -> None:
        self.id: str = ''
        self.items: List[Production] = []
        self.clousure: List[Production] = []
        self.type: str = type
        self.acceptance = False

    def change_acceptance(self) -> None:
        self.type = state_types.plain
        self.clousure = []
        self.items = []
        self.id = 'accept'
        self.acceptance = True
    
    def get_state_number(self) -> int:
        return int(self.id[1:])

    def state_label(self) -> str:
        if self.type == state_types.plain:
            return self.id
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