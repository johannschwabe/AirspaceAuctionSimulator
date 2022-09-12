from typing import Optional, Set

from Simulator.Allocations.AllocationReason import AllocationReason
from Simulator.Bids.Bid import Bid


class AllocationHistory:
    """
    Information about an allocation collected for statistics.
    """

    def __init__(self, bid: "Bid", compute_time: int, reason: "AllocationReason", explanation: str,
                 colliding_agent_ids: Optional[Set[str]] = None, displacing_agent_ids: Optional[Set[str]] = None):
        """
        Set the compute-time needed for this allocation, the reason for this allocation and the optional list of
        agents that are reallocated because of this allocation.
        :param bid:
        :param compute_time:
        :param reason:
        :param explanation:
        :param colliding_agent_ids:
        :param displacing_agent_ids:
        """
        self.bid: "Bid" = bid
        self.compute_time: int = compute_time
        self.reason: str = str(reason.value)
        self.explanation: str = explanation
        self.colliding_agent_ids: Optional[Set[str]] = colliding_agent_ids
        self.displacing_agent_ids: Optional[Set[str]] = displacing_agent_ids
