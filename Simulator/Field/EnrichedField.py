from ..Coordinate import TimeCoordinate


class EnrichedField:
    def __init__(self, coordinate: TimeCoordinate, cost: float):
        self.coordinate = coordinate
        self.cost = cost
