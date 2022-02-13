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
        local_env = self.env.clone()
        local_env.agents = []
        local_env.relevant_fields = {}
        local_env.agents = []
        self.allocator.env = local_env
        self.allocator.allocate_for_agent(local_agent)
        return local_agent.value_of_path(local_agent.allocated_path)

    def non_colliding_values(self):
        for agent in self.env.agents:
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.value_of_path(agent.allocated_path)}")
