from .ValueFunction import ValueFunction


class IndifferentValueFunction(ValueFunction):

    def __init__(self):
        super().__init__(None)

    def __call__(self, point_of_interest, **kwargs):
        return 1.0
