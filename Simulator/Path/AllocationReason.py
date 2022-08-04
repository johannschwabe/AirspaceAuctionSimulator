from typing import List, Optional

from Simulator.Path.Reason import Reason


class AllocationReason:
    def __init__(self, reason: str, colliding_agents_ids: Optional[List[int]] = None):
        self.reason: str = reason
        self.colliding_agents_ids: Optional[List[int]] = colliding_agents_ids
