from ..Simulator import Owner
from ..Simulator import Simulator
from ..Agent import Agent


class Statistics:
    def __init__(self, sim: Simulator):
        self.env = sim.environment
        self.allocator = sim.allocator
        self.history = sim.history
        self.owners = sim.owners
        self.time_elapsed = sim.time_step

    def non_colliding_value(self, agent: Agent):
        local_agent = agent.clone()
        local_env = self.env.clear()
        paths = self.allocator.allocate_for_agent(local_agent, local_env)
        return local_agent.value_for_paths(paths)

    def non_colliding_values(self):
        for agent in self.env.agents:
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.value_for_paths(agent.allocated_paths)}")

    @staticmethod
    def agents_welfare(agent: Agent):
        return agent.value_for_paths(agent.allocated_paths)

    def average_agents_welfare(self):
        summed_welfare = 0
        for agent in self.env.agents:
            summed_welfare += Statistics.agents_welfare(agent)
        return summed_welfare / len(self.env.agents)

    @staticmethod
    def owners_welfare(owner: Owner):
        summed_welfare = 0
        for agent in owner.agents:
            summed_welfare += Statistics.agents_welfare(agent)
        return summed_welfare
