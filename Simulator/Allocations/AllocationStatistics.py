from typing import List, Optional


class AllocationStatistics:
    """
    Information about an allocation collected for statistics.
    """

    def __init__(self, compute_time: int, reason: str, colliding_agent_ids: Optional[List[str]] = None):
        """
        Set the compute-time needed for this allocation, the reason for this allocation and the optional list of
        agents that are reallocated because of this allocation.
        :param compute_time:
        :param reason:
        :param colliding_agent_ids:
        """
        self.compute_time: int = compute_time
        self.reason: str = reason
        self.colliding_agent_ids: List[str] = colliding_agent_ids if colliding_agent_ids is not None else []
