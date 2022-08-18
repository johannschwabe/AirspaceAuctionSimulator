from abc import ABC, abstractmethod


class Segment(ABC):
    @abstractmethod
    def clone(self):
        pass
