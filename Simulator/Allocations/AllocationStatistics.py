from typing import List, Optional

from Simulator.Allocations.AllocationReason import AllocationReason


class AllocationStatistics:
    """
    Information about an allocation collected for statistics.
    """

    def __init__(self, compute_time: int, reason: "AllocationReason", explanation: str,
                 colliding_agent_ids: Optional[List[str]] = None, displacing_agent_id: Optional[str] = None):
        """
        Set the compute-time needed for this allocation, the reason for this allocation and the optional list of
        agents that are reallocated because of this allocation.
        :param compute_time:
        :param explanation:
        :param colliding_agent_ids:
        """
        self.compute_time: int = compute_time
        self.reason: str = str(reason.value())
        self.explanation: str = explanation
        self.colliding_agent_ids: Optional[List[str]] = colliding_agent_ids
        self.displacing_agent_id: Optional[str] = displacing_agent_id
