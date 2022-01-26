from typing import Dict

from simulator.agents import Agent
from Field import Field


class EnrichedField:
    def __init__(self, field: Field, blocked_probability: float):
        self.field: Field = field
        self.blocked_probability: float = blocked_probability

    def is_blocked(self) -> float:
        pass

    def allocated_to(self) -> Agent:
        pass

    def get_bid(self) -> Dict:
        return self.field.bid.public_info()

    def is_occupied(self) -> bool:
        return self.field.is_occupied()

    def is_allocated(self) -> bool:
        return self.field.is_allocated()

    def is_free_for_agent(self, agent: Agent) -> bool:
        return not self.is_blocked() and \
                (not self.is_occupied() or self.field.occupied_by == agent) and \
                (not self.is_allocated() or self.field.allocated_to == agent)
