from abc import ABC, abstractmethod

from Demos.CBS.Allocator.CBSAllocatorHelpers import HighLevelNode


class CostFunction(ABC):
    """
    The cost function CBS should optimize
    """
    failed_allocation_valid = False  # Whether an allocation where not all agents have a path is valid

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def __call__(node: "HighLevelNode") -> float:
        pass


class PathLength(CostFunction):
    """
    Minimize the total number of allocated ticks
    """
    failed_allocation_valid = False

    @staticmethod
    def __call__(node: "HighLevelNode") -> int:
        total_path_length = 0
        for path_segements in node.solution.values():
            for segment in path_segements:
                total_path_length += len(segment.coordinates)
        return total_path_length


class Welfare(CostFunction):
    """
    Minimize the negative summed value of all agents
    """
    failed_allocation_valid = True

    @staticmethod
    def __call__(node: "HighLevelNode") -> float:
        total_welfare = 0.0
        for agent in node.solution.keys():
            total_welfare += agent.value_for_segments(node.solution[agent])
        return -total_welfare  # nodes with lower cost are investigated first, thus negative welfare
