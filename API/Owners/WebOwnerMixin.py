from abc import ABC
from typing import List


class WebOwnerMixin(ABC):
    def __init__(self,
                 name: str,
                 color: str,
                 creation_ticks: List[int],
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = name
        self.color: str = color
        self.creation_ticks: List[int] = creation_ticks
