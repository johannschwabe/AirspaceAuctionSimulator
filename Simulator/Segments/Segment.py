from abc import ABC, abstractmethod
from typing import Tuple


class Segment(ABC):
    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def split_temporal(self, t: int) -> Tuple["Segment", "Segment"]:
        pass
