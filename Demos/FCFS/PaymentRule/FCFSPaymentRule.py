from typing import Dict

from Simulator import PaymentRule, Agent, Allocation
from ..BidTracker.FCFSBidTracker import FCFSBidTracker


class FCFSPaymentRule(PaymentRule):
    """
    Payment rule for FCFS Allocator. Multiplies each allocated voxel by configurable multiplier.
    """

    def __init__(self, voxel_multiplier: float = 1.):
        """
        Configurable multiplier.
        :param voxel_multiplier:
        """
        self.x = voxel_multiplier

    def calculate_payments(self, allocations: Dict["Agent", "Allocation"], bid_tracker: "FCFSBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for allocation in allocations.values():
            for segment in allocation.segments:
                allocation.payment += segment.nr_voxels * self.x
