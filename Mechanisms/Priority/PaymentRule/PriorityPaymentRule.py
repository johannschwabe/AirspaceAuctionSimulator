from typing import List

from Mechanisms.Priority.BidTracker.PriorityBidTracker import PriorityBidTracker
from Simulator.Allocations.Allocation import Allocation
from Simulator.Mechanism.PaymentRule import PaymentRule


class PriorityPaymentRule(PaymentRule):
    def __init__(self, voxel_multiplier: float = 1.):
        self.x = voxel_multiplier

    def calculate_payments(self, allocations: List[Allocation], bid_tracker: PriorityBidTracker):
        for allocation in allocations:
            for segment in allocation.segments:
                allocation.payment += segment.nr_voxels * self.x * bid_tracker.max_prio(allocation.agent)
