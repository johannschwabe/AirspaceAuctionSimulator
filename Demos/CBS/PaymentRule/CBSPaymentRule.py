from typing import Dict, TYPE_CHECKING

from Simulator import Allocation, PaymentRule

if TYPE_CHECKING:
    from Demos.CBS.BidTracker.CBSBidTracker import CBSBidTracker
    from Simulator import Allocation, Environment, Agent


class CBSPaymentRule(PaymentRule):
    """
    Payment rule for FCFS Allocator. Multiplies each allocated voxel by configurable multiplier.
    """
    label = "CBS Payment"

    def __init__(self, voxel_multiplier: float = 0.002):
        """
        Configurable multiplier.
        :param voxel_multiplier:
        """
        self.voxel_cost = voxel_multiplier

    def calculate_preliminary_payments(self, allocations: Dict["Agent", "Allocation"], bid_tracker: "CBSBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for allocation in allocations.values():
            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * self.voxel_cost

    def calculate_final_payments(self, environment: "Environment", bid_tracker: "CBSBidTracker"):
        res = {}
        for agent in environment.agents.values():
            for segment in agent.allocated_segments:
                if agent not in res:
                    res[hash(agent)] = 0
                res[hash(agent)] += segment.nr_voxels * self.voxel_cost
        return res
