from ..Coordinate import TimeCoordinate


class SpaceSegment:
    def __init__(self, mini: TimeCoordinate, maxi: TimeCoordinate):
        self.min = mini
        self.max = maxi
