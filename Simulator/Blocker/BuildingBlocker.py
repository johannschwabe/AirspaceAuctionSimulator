
from . import Blocker
from .. import Tick
from ..Coordinate import TimeCoordinate


class BuildingBlocker(Blocker):
    def __init__(self, location: TimeCoordinate, vertices):
        locations = [TimeCoordinate(0,0,0, Tick(-t)) + location for t in range(location.t+1)][::-1]
        bbox = vertices["bounds"]
        self.points = vertices["coords"]
        super().__init__(locations, bbox)


    @staticmethod
    def is_blocking(coord: TimeCoordinate):
        return True
