from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ..Agents.Agent import Agent


class Bid(ABC):
    def __init__(self, agent: "Agent"):
        self.agent: "Agent" = agent

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, str | int | float]:
        pass
