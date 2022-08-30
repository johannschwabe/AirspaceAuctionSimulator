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
    """
    The simulator class.
    """

    def __init__(self, owners: List["Owner"], mechanism: "Mechanism", environment: "Environment"):
        """
        Initialize all parts of the simulation.
        Time-steps start at 0.
        :param owners:
        :param mechanism:
        :param environment:
        """
        self.owners: List["Owner"] = owners
        self.mechanism: "Mechanism" = mechanism
        self.environment: "Environment" = environment
        self.history: "History" = History()

        self.time_step = 0

    def generate_new_agents(self) -> Dict[int, "Agent"]:
        """
        Ask all owners for new agents to join this time-step.
        :return:
        """
        new_agents: Dict[int, "Agent"] = {}
        for owner in self.owners:
            generated_agents = owner.generate_agents(self.time_step, self.environment)
            for generated_agent in generated_agents:
                new_agents[hash(generated_agent)] = generated_agent
        return new_agents

    def tick(self) -> bool:
        """
        Execute one tick of the simulation.
        Returns `True` until the simulation is done, then it returns `False`.
        :return:
        """
        if self.time_step > self.environment.dimension.t:
            return False

        new_agents: Dict[int, "Agent"] = self.generate_new_agents()

        if len(new_agents) > 0 or self.mechanism.allocator.wants_to_reallocate():
            start_time = time_ns()

            self.history.add_new_agents(list(new_agents.values()), self.time_step)
            temporary_environment = self.environment.clone()
            temporary_agents = [agent.clone() for agent in new_agents.values()]
            temporary_allocations: Dict["Agent", "Allocation"] = self.mechanism.do(
                temporary_agents,
                temporary_environment,
                self.time_step)
            real_allocations = self.environment.create_real_allocations(list(temporary_allocations.values()),
                                                                        new_agents)
            self.environment.allocate_segments_for_agents(real_allocations, self.time_step)
            self.history.update_allocations(real_allocations, self.time_step, time_ns() - start_time)

            print(f"STEP: {self.time_step}")
            print("-------------")

        self.time_step += 1
        return True
