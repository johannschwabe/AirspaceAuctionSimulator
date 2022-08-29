from typing import List, TYPE_CHECKING

from Simulator.Mechanism.PaymentRule import PaymentRule

if TYPE_CHECKING:
    from Demos.Priority.BidTracker.PriorityBidTracker import PriorityBidTracker
    from Simulator.Allocations.Allocation import Allocation
    from Simulator.Environment.Environment import Environment


class PriorityPaymentRule(PaymentRule):
    label = "Priority Payment"

    def __init__(self, voxel_multiplier: float = 1.):
        self.voxel_cost = voxel_multiplier

    def calculate_preliminary_payments(self, allocations: List["Allocation"], bid_tracker: "PriorityBidTracker"):
        for allocation in allocations:
            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * self.voxel_cost * bid_tracker.max_prio(
                    allocation.agent)

    def calculate_final_payments(self, environment: "Environment", bid_tracker: "PriorityBidTracker"):
        res = {}
        for agent in environment.agents.values():
            for segment in agent.allocated_segments:
                if agent not in res:
                    res[agent] = 0
                res[agent] += segment.nr_voxels * self.voxel_cost * bid_tracker.max_prio(agent)
        return res
