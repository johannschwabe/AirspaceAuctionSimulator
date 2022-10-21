from typing import Dict, TYPE_CHECKING

from Simulator import PaymentRule
from Simulator.Agents.PathAgent import PathAgent

if TYPE_CHECKING:
    from ..BidTracker.PriorityBidTracker import PriorityBidTracker
    from Simulator import Allocation, Environment, Agent


class PriorityPaymentRule(PaymentRule):
    """
    Payment rule for Priority Allocator. Multiplies each allocated voxel by configurable multiplier and the
    max priority of any bid the agent placed.
    """

    label = "Priority Payment"

    def __init__(self, path_voxel_multiplier: float = 0.2, space_voxel_multiplier: float = 0.00005):
        """
        Configurable multipliers.
        :param path_voxel_multiplier: base cost of a voxel for path agents
        :param space_voxel_multiplier: base cost of a voxel for space agents
        """
        self.path_voxel_cost = path_voxel_multiplier
        self.space_voxel_cost = space_voxel_multiplier

    def calculate_preliminary_payments(self, allocations: Dict["Agent", "Allocation"],
                                       bid_tracker: "PriorityBidTracker"):
        """
        Calculates the payment by multiplying #voxels with multiplier x and the max priority of the agents bids.
        :param allocations:
        :param bid_tracker:
        :return:
        """
        for _agent, allocation in allocations.items():
            max_prio = bid_tracker.max_prio(_agent)
            voxel_cost = self.path_voxel_cost if isinstance(_agent, PathAgent) else self.space_voxel_cost
            for segment in allocation.segments:
                allocation.preliminary_payment += segment.nr_voxels * voxel_cost * max_prio

    def calculate_final_payments(self,
                                 environment: "Environment",
                                 bid_tracker: "PriorityBidTracker") -> Dict[int, float]:
        res: Dict[int, float] = {}
        for agent in environment.agents.values():
            max_prio = bid_tracker.max_prio(agent)
            res[hash(agent)] = 0
            voxel_cost = self.path_voxel_cost if isinstance(agent, PathAgent) else self.space_voxel_cost
            for segment in agent.allocated_segments:
                res[hash(agent)] += segment.nr_voxels * voxel_cost * max_prio
        return res
