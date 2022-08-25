from typing import List, Optional


class AllocationStatistics:

    def __init__(self, compute_time: int, reason: str, colliding_agents_ids: Optional[List[int]] = None):
        self.compute_time: int = compute_time
        self.reason: str = reason
        self.colliding_agents_ids: Optional[List[int]] = colliding_agents_ids
