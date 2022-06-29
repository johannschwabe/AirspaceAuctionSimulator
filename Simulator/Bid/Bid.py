from abc import ABC


class Bid(ABC):
    def __init__(self, battery: int):
        self.battery: int = battery
