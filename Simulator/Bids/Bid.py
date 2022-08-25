from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent


class Bid(ABC):
    def __init__(self, agent: "Agent"):
        self.agent: "Agent" = agent
