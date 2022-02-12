from abc import ABC, abstractmethod


class ValueFunction(ABC):

    def __init__(self, optimum):
        self.optimum = optimum

    @abstractmethod
    def __call__(self, point_of_interest, **kwargs):
        pass
