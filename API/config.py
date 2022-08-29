from Demos.FCFS.Allocator.FCFSAllocator import FCFSAllocator
from Demos.FCFS.ValueFunction.FCFSPathValueFunction import FCFSPathValueFunction
from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Demos.Priority.Allocator.PriorityAllocator import PriorityAllocator
from Demos.Priority.ValueFunction.PriorityPathValueFunction import PriorityPathValueFunction
from Demos.Priority.ValueFunction.PrioritySpaceValueFunction import PrioritySpaceValueFunction

available_allocators = [PriorityAllocator, FCFSAllocator]

available_value_functions = [FCFSPathValueFunction, FCFSSpaceValueFunction, PriorityPathValueFunction,
                             PrioritySpaceValueFunction]
