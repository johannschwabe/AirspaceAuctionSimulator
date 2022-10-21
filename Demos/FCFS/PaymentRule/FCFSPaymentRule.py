from typing import Dict, TYPE_CHECKING

from Simulator import Allocation, PaymentRule
from Simulator.Agents.PathAgent import PathAgent
from ..BidTracker.FCFSBidTracker import FCFSBidTracker

if TYPE_CHECKING:
    from Simulator import Allocation, Environment, Agent
    from ..BidTracker.FCFSBidTracker import FCFSBidTracker


class FCFSPaymentRule(PaymentRule):
    """
    Payment rule for FCFS Allocator. Multiplies each allocated voxel by configurable multiplier.
    """
    label = "FCFS Payment"

    def __init__(self, path_voxel_multiplier: float = 0.2, space_voxel_multiplier: float = 0.00005):
        """
        Configurable multipliers.
        :param path_voxel_multiplier:
        :param space_voxel_multiplier:
        """
        self.path_voxel_cost = path_voxel_multiplier
        self.space_voxel_cost = space_voxel_multiplier

    def calculate_preliminary_payments(self, allocations: Dict["Agent", "Allocation"], bid_tracker: "FCFSBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for _agent, allocation in allocations.items():
            voxel_cost = self.path_voxel_cost if isinstance(_agent, PathAgent) else self.space_voxel_cost

            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * voxel_cost

    def calculate_final_payments(self, environment: "Environment", bid_tracker: "FCFSBidTracker") -> Dict[int, float]:
        res: Dict[int, float] = {}
        for agent in environment.agents.values():
            res[hash(agent)] = 0
            voxel_cost = self.path_voxel_cost if isinstance(agent, PathAgent) else self.space_voxel_cost

            for segment in agent.allocated_segments:
                res[hash(agent)] += segment.nr_voxels * voxel_cost
        return res
