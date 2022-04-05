from .Environment import Environment
from ..Coordinate import TimeCoordinate
from ..Field import Field

class TempEnvironment(Environment):
    def __init__(self, env: Environment):
        self.env = env
        super().__init__(env._dimension, env.blockers)

    def get_field_at(self, coords: TimeCoordinate, creating: bool) -> Field:
        key = coords.get_key()
        if key in self._relevant_fields:
            return self._relevant_fields[key]
        if key in self.env._relevant_fields:
            real_field = self.env._relevant_fields[key]
            new_field= Field(coords)
            for agent in real_field.get_allocated():
                if agent in self._agents:
                    new_field.add_allocation(self._agents[self._agents.index(agent)])
                else:
                    cloned_agent = agent.clone()
                    new_field.add_allocation(cloned_agent)
                    self._agents.append(cloned_agent)
            for agent in real_field.get_near():
                if agent in self._agents:
                    new_field.add_near(self._agents[self._agents.index(agent)])
                else:
                    cloned_agent = agent.clone()
                    new_field.add_near(cloned_agent)
                    self._agents.append(cloned_agent)
            for agent in real_field.get_far():
                if agent in self._agents:
                    new_field.add_far(self._agents[self._agents.index(agent)])
                else:
                    cloned_agent = agent.clone()
                    new_field.add_far(cloned_agent)
                    self._agents.append(cloned_agent)
        else:
            new_field = Field(coords)

        if creating:
            self._relevant_fields[key] = new_field
        return new_field
