from typing import List

from Simulator import PaymentRule, Allocation
from ..BidTracker.FCFSBidTracker import FCFSBidTracker


class FCFSPaymentRule(PaymentRule):
    def __init__(self, voxel_multiplier: float = 1.):
        self.x = voxel_multiplier

    def calculate_payments(self, allocations: List[Allocation], bid_tracker: FCFSBidTracker):
        for allocation in allocations:
            for segment in allocation.segments:
                allocation.payment += segment.nr_voxels * self.x
