from typing import TYPE_CHECKING, Dict

from Simulator import PaymentRule

if TYPE_CHECKING:
    from ..BidTracker.PriorityBidTracker import PriorityBidTracker
    from Simulator import Allocation, Environment, Agent


class PriorityPaymentRule(PaymentRule):
    """
    Payment rule for Priority Allocator. Multiplies each allocated voxel by configurable multiplier and the
    max priority of any bid the agent placed.
    """

    label = "Priority Payment"

    def __init__(self, voxel_multiplier: float = 1.):
        """
        Configurable multiplier.
        :param voxel_multiplier:
        """
        self.voxel_cost = voxel_multiplier

    def calculate_preliminary_payments(self, allocations: Dict["Agent", "Allocation"],
                                       bid_tracker: "PriorityBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x and the max priority of the agents bids.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for allocation in allocations.values():
            max_prio = bid_tracker.max_prio(allocation.agent)
            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * self.voxel_cost * max_prio

    def calculate_final_payments(self,
                                 environment: "Environment",
                                 bid_tracker: "PriorityBidTracker") -> Dict[int, float]:
        res: Dict[int, float] = {}
        for agent in environment.agents.values():
            max_prio = bid_tracker.max_prio(agent)
            res[hash(agent)] = 0
            for segment in agent.allocated_segments:
                res[hash(agent)] += segment.nr_voxels * self.voxel_cost * max_prio
        return res
