from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Allocation.AllocationReason import AllocationReason
    from ..Allocation.Segment import Segment


class HistoryAgent:
    def __init__(self, agent: "Agent", registered: int):
        self.id: int = agent.id
        self.registered: int = registered
        self.past_allocations: Dict[int, Dict[str, List[List["Coordinate4D"]] | "AllocationReason" | int]] = {}

    def reallocation(self, new_path: List["Segment"], reason: "AllocationReason", time_step: int, compute_time: int):
        self.past_allocations[time_step] = {"path": new_path, "reason": reason, "time": compute_time}
