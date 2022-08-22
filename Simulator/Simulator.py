from time import time_ns
from typing import List, TYPE_CHECKING, Dict

from .History.History import History

if TYPE_CHECKING:
    from .Allocation.Allocation import Allocation
    from .Agents.Agent import Agent
    from .Environment.Environment import Environment
    from .Allocator.Allocator import Allocator
    from .Owners.Owner import Owner


class Simulator:
    def __init__(self,
                 owners: List["Owner"],
                 allocator: "Allocator",
                 environment: "Environment"):
        self.owners: List["Owner"] = owners
        self.allocator: "Allocator" = allocator
        self.environment: "Environment" = environment
        self.history: "History" = History(allocator, environment, owners)

        self.time_step = 0
        self._agent_id = 0

    def get_agent_id(self) -> int:
        agent_id = self._agent_id
        self._agent_id += 1
        return agent_id

    def generate_new_agents(self) -> Dict[int, "Agent"]:
        new_agents: Dict[int, "Agent"] = {}
        for owner in self.owners:
            generated_agents = owner.generate_agents(self.time_step, self)
            for generated_agent in generated_agents:
                new_agents[generated_agent.id] = generated_agent
        return new_agents

    def tick(self):
        new_agents: Dict[int, "Agent"] = self.generate_new_agents()

        if len(new_agents) > 0:
            start_time = time_ns()

            self.history.add_new_agents(list(new_agents.values()), self.time_step)
            temporary_environment = self.environment.clone()
            temporary_allocations: List["Allocation"] = self.allocator.allocate(
                list(new_agents.values()),
                temporary_environment,
                self.time_step)
            real_allocations = self.environment.create_real_allocations(temporary_allocations, new_agents)
            self.environment.allocate_segments_for_agents(real_allocations, self.time_step)
            self.history.update_allocations(real_allocations, self.time_step, time_ns() - start_time)
            print(f"STEP: {self.time_step}")
            print("-------------")

        self.time_step += 1
