from typing import List, TYPE_CHECKING, Dict

from Simulator import Allocation
from ..BidTracker.FCFSBidTracker import FCFSBidTracker
from Simulator import PaymentRule

if TYPE_CHECKING:
    from Simulator import Allocation, Environment, Agent
    from ..BidTracker.FCFSBidTracker import FCFSBidTracker


class FCFSPaymentRule(PaymentRule):
    """
    Payment rule for FCFS Allocator. Multiplies each allocated voxel by configurable multiplier.
    """
    label = "FCFS Payment"

    def __init__(self, voxel_multiplier: float = 1.):
        """
        Configurable multiplier.
        :param voxel_multiplier:
        """
        self.voxel_cost = voxel_multiplier

    def calculate_preliminary_payments(self, allocations: Dict["Agent", "Allocation"], bid_tracker: "FCFSBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for allocation in allocations.values():
            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * self.voxel_cost

    def calculate_final_payments(self, environment: "Environment", bid_tracker: "FCFSBidTracker"):
        res = {}
        for agent in environment.agents.values():
            for segment in agent.allocated_segments:
                if agent not in res:
                    res[agent] = 0
                res[agent] += segment.nr_voxels * self.voxel_cost
        return res
