from ..Coordinate import Coordinate4D


class SpaceSegment:
    def __init__(self, mini: Coordinate4D, maxi: Coordinate4D):
        self.min = mini
        self.max = maxi

    def clone(self):
        return SpaceSegment(self.min.clone(), self.max.clone())
