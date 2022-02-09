from .ValueFunction import ValueFunction


class RangeValueFunction(ValueFunction):

    def __init__(self, optimum, equi_valuable_range):
        super().__init__(optimum)
        self.equi_valuable_range = equi_valuable_range

    def difference(self, val_1, val_2) -> float:
        return float(abs(val_1 - val_2))

    def __call__(self, point_of_interest):
        diff = self.difference(self.optimum, point_of_interest)
        if diff < self.equi_valuable_range:
            return 1.0
        return 0.0
