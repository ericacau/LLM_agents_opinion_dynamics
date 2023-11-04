import random


class Agent(object):
    def __init__(self, name: str, status: float = None, **kwargs):
        """
        Initialize the Profile object.

        :param name: The name of the profile.
        :param age: The age of the profile.
        :param gender: The gender of the profile.
        """
        self.name = name
        self.profile = kwargs
        self.neighbors = {}
        self.status = status

    def get_status(self):
        return self.status

    def set_status(self, status: float):
        self.status = status

    def __str__(self):
        """
        Return a string representation of the Profile object.
        """
        return f"Name: {self.name}"

    def __dict__(self):
        """
        Return a dictionary representation of the Profile object.
        """
        return {"name": self.name, **self.profile}

    def add_neighbor(self, neighbor: object):
        self.neighbors[neighbor.name] = neighbor

    def add_neighbors(self, neighbors: list):
        for neighbor in neighbors:
            self.add_neighbor(neighbor)

    def get_neighbor(self, name: str):
        return self.neighbors[name]

    def get_random_neighbor(self):
        return random.choice(list(self.neighbors.values()))

    def get_neighbors(self):
        return list(self.neighbors.values())

    def neighbors_iter(self):
        for k, v in self.neighbors.items():
            yield k, v


class Agents(object):

    def __init__(self):
        self.agents = {}

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def get_agent(self, name: str):
        return self.agents[name]

    def add_agents(self, agents: list):
        for agent in agents:
            self.add_agent(agent)

    def get_random_agent(self):
        return random.choice(list(self.agents.values()))

    def agents_iter(self):
        for k, v in self.agents.items():
            yield k, v

