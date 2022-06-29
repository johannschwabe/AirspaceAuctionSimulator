from ..Coordinate import Coordinate4D


class SpaceSegment:
    def __init__(self, mini: Coordinate4D, maxi: Coordinate4D):
        self.min = mini
        self.max = maxi
