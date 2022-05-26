from typing import List

from . import Blocker
from .. import Tick
from ..Coordinate import TimeCoordinate


class BuildingBlocker(Blocker):
    def __init__(self, location: TimeCoordinate, vertices):
        locations = [TimeCoordinate(0,0,0, Tick(-t)) + location for t in range(location.t+1)][::-1]
        bbox = vertices["bounds"]
        print(locations)
        print(bbox)
        super().__init__(locations, bbox)


