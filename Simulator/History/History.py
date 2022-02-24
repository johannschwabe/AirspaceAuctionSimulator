from typing import List
from .Owner import Owner
from ..IO import Stringify
from ..Coordinate import TimeCoordinate


class History(Stringify):

    def __init__(self, dimensions: TimeCoordinate, owners: List[Owner]):
        self.dimensions: TimeCoordinate = dimensions
        self.owners: List[Owner] = owners

