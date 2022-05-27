from abc import ABC, abstractmethod
from typing import List
from ..Coordinate import TimeCoordinate

class Segment(ABC):
    def __init__(self, coordinates: List["TimeCoordinate"]):
        self.coordinates = coordinates
        self.__i = 0

    @abstractmethod
    def clone(self):
        pass

    def __getitem__(self, n):
        return self.coordinates[n]

    def __len__(self):
        return len(self.coordinates)

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < len(self.coordinates):
            loc = self.coordinates[self.__i]
            self.__i += 1
            return loc
        raise StopIteration
