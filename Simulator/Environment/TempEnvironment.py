from Simulator.Environment import Environment
from Simulator.Coordinate import TimeCoordinate
from Simulator.Field import Field

class TempEnvironment(Environment.Environment):
    def __init__(self, env: Environment):
        self.env = env
        super().__init__(env.dimension, env.blocker)

    def get_field_at(self, coords: TimeCoordinate, creating: bool) -> Field:
        key = coords.get_key()
        if key in self.relevant_fields:
            return self.relevant_fields[key]
        if key in self.env.relevant_fields:
            real_field = self.env.relevant_fields[key]
            new_field= Field(coords)
            for agent in real_field.allocated_to:
                if agent in self.agents:
                    new_field.allocated_to.append(self.agents[self.agents.index(agent)])
                else:
                    cloned_agent = agent.clone()
                    new_field.allocated_to.append(cloned_agent)
                    self.agents.append(cloned_agent)
            for agent in real_field.near_to:
                if agent in self.agents:
                    new_field.near_to.append(self.agents[self.agents.index(agent)])
                else:
                    cloned_agent = agent.clone()
                    new_field.near_to.append(cloned_agent)
                    self.agents.append(cloned_agent)
            for agent in real_field.far_to:
                if agent in self.agents:
                    new_field.far_to.append(self.agents[self.agents.index(agent)])
                else:
                    cloned_agent = agent.clone()
                    new_field.far_to.append(cloned_agent)
                    self.agents.append(cloned_agent)
        else:
            new_field = Field(coords)

        if creating:
            self.relevant_fields[key] = new_field
        return new_field
