from abc import ABC
from Simulator.Owner.Owner import Owner


class PathOwner(Owner, ABC):
    def __init__(self, name: str, color: str):
        super().__init__(name, color)
