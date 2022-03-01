from typing import List
from .Owner import Owner
from ..IO import Stringify
from ..Coordinate import TimeCoordinate
from .Environment import Environment


class History(Stringify):

    def __init__(self, name: str, description: str, dimensions: TimeCoordinate, owners: List[Owner]):
        self.name: str = name
        self.description: str = description
        self.environment: Environment = Environment(dimensions, 100)
        self.dimensions: TimeCoordinate = dimensions
        self.owners: List[Owner] = owners

