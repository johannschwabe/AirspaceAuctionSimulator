from ..Allocator import Allocator
from ..History import History
from ..Agent import Agent


class Statistics:
    def __init__(self, history: History, allocator: Allocator):
        self.env = history.environment
        self.allocator = allocator

    def non_colliding_value(self, agent: Agent):
        local_agent = agent.clone()
        local_env = self.env.clear()
        paths = self.allocator.allocate_for_agent(local_agent, local_env)
        return local_agent.value_for_paths(paths)

    def non_colliding_values(self):
        for agent in self.env._agents:
            print(f"{agent}'s non colliding value: {self.non_colliding_value(agent)}, "
                  f"achieved value: {agent.value_for_paths(agent._allocated_paths)}")
