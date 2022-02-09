from .ValueFunction import ValueFunction


class OnlyOneValueFunction(ValueFunction):

    def __init__(self, optimum):
        super().__init__(optimum)

    def is_same(self, val_1, val_2) -> bool:
        return val_1 == val_2

    def __call__(self, point_of_interest) -> float:
        if self.is_same(point_of_interest, self.optimum):
            return 1.0
        return 0.0

