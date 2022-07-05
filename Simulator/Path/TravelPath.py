from typing import List

from ..Coordinate import Coordinate4D


class TravelPath:

    def __init__(self, locations: List[Coordinate4D]):
        self.locations: List[Coordinate4D] = locations
        self.__i = 0

    def __getitem__(self, n):
        return self.locations[n]

    def __len__(self):
        return len(self.locations)

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < len(self.locations):
            loc = self.locations[self.__i]
            self.__i += 1
            return loc
        raise StopIteration
