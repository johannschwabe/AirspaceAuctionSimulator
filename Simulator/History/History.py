from typing import List
from .Owner import Owner
from ..IO import Stringify
from ..Coordinate import TimeCoordinate


class History(Stringify):

    def __init__(self, name: str, description: str, dimensions: TimeCoordinate, owners: List[Owner]):
        self.name: str = name
        self.description: str = description
        self.dimensions: TimeCoordinate = dimensions
        self.owners: List[Owner] = owners

