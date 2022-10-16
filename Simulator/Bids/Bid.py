from abc import ABC, abstractmethod
from typing import Any, Dict, TYPE_CHECKING

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
    def __ge__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
