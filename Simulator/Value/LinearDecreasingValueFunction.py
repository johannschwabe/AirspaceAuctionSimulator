from .ValueFunction import ValueFunction


def difference(val_1, val_2) -> float:
    return float(abs(val_1 - val_2))


class LinearDecreasingValueFunction(ValueFunction):

    def __init__(self, optimum, distance_to_zero):
        super().__init__(optimum)
        assert distance_to_zero > 0, "Distance to zero can't be 0."
        self.distance_to_zero = distance_to_zero

    def __call__(self, point_of_interest, **kwargs):
        diff = difference(self.optimum, point_of_interest)
        if diff > self.distance_to_zero:
            return 0.0
        return 1.0 - (diff / self.distance_to_zero)
