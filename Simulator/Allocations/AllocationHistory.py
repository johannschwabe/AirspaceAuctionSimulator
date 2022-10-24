from typing import Dict, Optional

from Simulator.Allocations.AllocationReason import AllocationReason
from Simulator.Bids.Bid import Bid


class AllocationHistory:
    """
    Information about an allocation collected for statistics.
    """

    def __init__(self,
                 bid: "Bid",
                 compute_time: int,
                 reason: "AllocationReason",
                 explanation: str,
                 colliding_agent_bids: Optional[Dict[str, "Bid"]] = None,
                 displacing_agent_bids: Optional[Dict[str, "Bid"]] = None):
        """
        Set the compute-time needed for this allocation, the reason for this allocation and the optional list of
        agents that are reallocated because of this allocation.
        :param bid:
        :param compute_time:
        :param reason:
        :param explanation:
        :param colliding_agent_bids:
        :param displacing_agent_bids:
        """
        self.bid: "Bid" = bid
        self.compute_time: int = compute_time
        self.reason: str = str(reason.value)
        self.explanation: str = explanation
        self.colliding_agent_bids: Optional[Dict[str, "Bid"]] = colliding_agent_bids
        self.displacing_agent_bids: Optional[Dict[str, "Bid"]] = displacing_agent_bids
