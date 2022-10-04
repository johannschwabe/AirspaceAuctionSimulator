from abc import ABC, abstractmethod

from Demos.CBS.Allocator.CBSAllocatorHelpers import HighLevelNode


class CostFunction(ABC):
    failed_allocation_valid = False

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def __call__(node: "HighLevelNode"):
        pass


class PathLength(CostFunction):
    failed_allocation_valid = False

    @staticmethod
    def __call__(node: "HighLevelNode"):
        total_path_length = 0
        for path_segements in node.solution.values():
            for segment in path_segements:
                total_path_length += len(segment.coordinates)
        return total_path_length


class Welfare(CostFunction):
    failed_allocation_valid = True

    @staticmethod
    def __call__(node: "HighLevelNode"):
        total_welfare = 0.0
        for agent in node.solution.keys():
            total_welfare += agent.value_for_segments(node.solution[agent])
        return -total_welfare  # nodes with lower welfare are investigated first, thus negative welfare
