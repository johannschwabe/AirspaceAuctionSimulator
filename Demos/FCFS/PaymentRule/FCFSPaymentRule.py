from typing import List, TYPE_CHECKING

from Simulator.Mechanism.PaymentRule import PaymentRule

if TYPE_CHECKING:
    from Simulator.Allocations.Allocation import Allocation
    from Simulator.Environment.Environment import Environment


class FCFSPaymentRule(PaymentRule):
    label = "FCFS Payment"

    def __init__(self, voxel_multiplier: float = 1.):
        self.voxel_cost = voxel_multiplier

    def calculate_preliminary_payments(self, allocations: List["Allocation"], _=None):
        for allocation in allocations:
            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * self.voxel_cost

    def calculate_final_payments(self, environment: "Environment", _):
        res = {}
        for agent in environment.agents.values():
            for segment in agent.allocated_segments:
                if agent not in res:
                    res[agent] = 0
                res[agent] += segment.nr_voxels * self.voxel_cost
        return res
