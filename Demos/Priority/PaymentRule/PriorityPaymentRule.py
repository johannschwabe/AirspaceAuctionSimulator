from typing import Dict

from Simulator import Allocation, PaymentRule, Agent
from ..BidTracker.PriorityBidTracker import PriorityBidTracker


class PriorityPaymentRule(PaymentRule):
    """
    Payment rule for Priority Allocator. Multiplies each allocated voxel by configurable multiplier and the
    max priority of any bid the agent placed.
    """

    def __init__(self, voxel_multiplier: float = 1.):
        """
        Configurable multiplier.
        :param voxel_multiplier:
        """
        self.x = voxel_multiplier

    def calculate_payments(self, allocations: Dict["Agent", "Allocation"], bid_tracker: "PriorityBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x and the max priority of the agents bids.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for allocation in allocations.values():
            max_prio = bid_tracker.max_prio(allocation.agent)
            for segment in allocation.segments:
                allocation.payment += segment.nr_voxels * self.x * max_prio
