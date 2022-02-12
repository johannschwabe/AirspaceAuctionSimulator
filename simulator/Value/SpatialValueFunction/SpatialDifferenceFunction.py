from simulator.coordinates import Coordinate


class SpatialDifferenceFunction:
    def __init__(self, norm):
        self.norm = norm

    def difference(self, val_1: Coordinate, val_2: Coordinate) -> float:
        return getattr(val_2 - val_1, self.norm)