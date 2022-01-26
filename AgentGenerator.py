from abc import abstractmethod, ABC

from Environment import Environment


class AgentGenerator(ABC):
    def __init__(self, env: Environment):
        self.env = env

    @abstractmethod
    def reset(self):
        pass

    # list of new Agents to be added into the simulation befor time_step
    @abstractmethod
    def update_agents(self, time_step):
        pass
