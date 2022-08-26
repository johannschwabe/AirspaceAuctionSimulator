from time import time_ns
from typing import List, TYPE_CHECKING, Dict

from .History.History import History

if TYPE_CHECKING:
    from .Allocations.Allocation import Allocation
    from .Agents.Agent import Agent
    from .Environment.Environment import Environment
    from .Owners.Owner import Owner
    from .Mechanism.Mechanism import Mechanism


class Simulator:
    def __init__(self,
                 owners: List["Owner"],
                 mechanism: "Mechanism",
                 environment: "Environment"):
        self.owners: List["Owner"] = owners
        self.mechanism: "Mechanism" = mechanism
        self.environment: "Environment" = environment
        self.history: "History" = History()

        self.time_step = 0
        self._agent_id = 0

    def get_agent_id(self) -> int:
        agent_id = self._agent_id
        self._agent_id += 1
        return agent_id

    def generate_new_agents(self) -> Dict[int, "Agent"]:
        new_agents: Dict[int, "Agent"] = {}
        for owner in self.owners:
            generated_agents = owner.generate_agents(self.time_step, self.environment)
            for generated_agent in generated_agents:
                new_agents[hash(generated_agent)] = generated_agent
        return new_agents

    def tick(self) -> bool:
        if self.time_step > self.environment.dimension.t:
            return False

        new_agents: Dict[int, "Agent"] = self.generate_new_agents()

        start_time = time_ns()

        self.history.add_new_agents(list(new_agents.values()), self.time_step)
        temporary_environment = self.environment.clone()
        temporary_agents = [agent.clone() for agent in new_agents.values()]
        temporary_allocations: List["Allocation"] = self.mechanism.do(
            temporary_agents,
            temporary_environment,
            self.time_step)
        real_allocations = self.environment.create_real_allocations(temporary_allocations, new_agents)
        self.environment.allocate_segments_for_agents(real_allocations, self.time_step)
        self.history.update_allocations(real_allocations, self.time_step, time_ns() - start_time)

        if len(temporary_allocations) > 0:
            print(f"STEP: {self.time_step}")
            print("-------------")

        self.time_step += 1
        return True
