from typing import List, Optional

from Simulator.Allocations.AllocationType import AllocationType


class AllocationStatistics:
    """
    Information about an allocation collected for statistics.
    """

    def __init__(self, compute_time: int, allocation_type: "AllocationType", reason: str,
                 colliding_agent_ids: Optional[List[str]] = None, displacing_agent_id: Optional[str] = None):
        """
        Set the compute-time needed for this allocation, the reason for this allocation and the optional list of
        agents that are reallocated because of this allocation.
        :param compute_time:
        :param reason:
        :param colliding_agent_ids:
        """
        self.compute_time: int = compute_time
        self.type: "AllocationType" = allocation_type
        self.reason: str = reason
        self.colliding_agent_ids: Optional[List[str]] = colliding_agent_ids
        self.displacing_agent_id: Optional[str] = displacing_agent_id
