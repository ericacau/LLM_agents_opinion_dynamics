import random


class Agent(object):
    def __init__(self, name: str, status: int = None, **kwargs):
        """
        Initialize the Agent object.

        :param name: name of the agent
        :param status: status of the agent, integer between 1 and 10
        :param kwargs: additional parameters
        """
        self.name = name
        self.profile = kwargs
        self.neighbors = {}
        self.status = status
        self.args = kwargs

    def get_status(self) -> int:
        """
        Return the status of the agent

        :return: status of the agent
        """
        return self.status

    def set_status(self, status: float):
        """
        Set the status of the agent

        :param status: status of the agent, integer between 1 and 10
        """
        self.status = status

    def __str__(self) -> str:
        """
        Return a string representation of the Profile object.

        :return: agent representation
        """
        return f"Name: {self.name}, Status: {self.status}"

    def __dict__(self) -> dict:
        """
        Return a dictionary representation of the Profile object.

        :return: agent representation
        """
        return {"name": self.name, **self.profile}

    def add_neighbor(self, neighbor: object):
        """
        Add a neighbor to the agent

        :param neighbor: an Agent object
        """
        self.neighbors[neighbor.name] = neighbor

    def add_neighbors(self, neighbors: list):
        """
        Add a list of neighbors to the agent

        :param neighbors: a list of Agent objects
        """
        for neighbor in neighbors:
            self.add_neighbor(neighbor)

    def get_neighbor(self, name: str) -> object:
        """
        Get a neighbor by name

        :param name: name of the neighbor
        :return: an Agent object
        """
        return self.neighbors[name]

    def get_random_neighbor(self) -> object:
        """
        Get a random neighbor

        :return: an Agent object
        """
        return random.choice(list(self.neighbors.values()))

    def get_neighbors(self) -> list:
        """
        Get all the neighbors of the agent

        :return: a lis of Agent objects
        """
        return list(self.neighbors.values())

    def neighbors_iter(self) -> object:
        """
        Iterate over the neighbors of the agent

        :return: an iterator over the neighbors of the agent
        """
        for k, v in self.neighbors.items():
            yield k, v


class Agents(object):
    def __init__(self):
        """
        Initialize the Agents object.
        """
        self.agents = {}

    def add_agent(self, agent: Agent):
        """
        Add an agent to the Agents object

        :param agent: an Agent object
        """
        self.agents[agent.name] = agent

    def get_agent(self, name: str) -> object:
        """
        Get an agent by name

        :param name: name of the agent
        :return: an Agent object
        """
        return self.agents[name]

    def add_agents(self, agents: list):
        """
        Add a list of agents to the Agents object

        :param agents: a list of Agent objects
        """
        for agent in agents:
            self.add_agent(agent)

    def get_random_agent(self) -> object:
        """
        Get a random agent

        :return: an Agent object
        """
        return random.choice(list(self.agents.values()))

    def agents_iter(self) -> (str, Agent):
        """
        Iterate over the agents

        :return: an iterator over (name, Agent) pairs
        """
        for k, v in self.agents.items():
            yield k, v
