from abc import ABC, abstractmethod

from ..Agent import Agent
from ..Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agent(self, agent: Agent, env: Environment):
        pass
