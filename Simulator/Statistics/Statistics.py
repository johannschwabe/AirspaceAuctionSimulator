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
        path = self.allocator.allocate_for_agent(local_agent, local_env)
        return local_agent.value_for_paths(path)

    def non_colliding_values(self):
        for agent in self.env.agents:
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.value_for_paths(agent.allocated_paths)}")
