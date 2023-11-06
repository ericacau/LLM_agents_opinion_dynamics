import random


class Agent(object):
    def __init__(self, name: str, status: int = None, **kwargs):
        """
        Initialize the Agent object.

        :param name:
        :param status:
        :param kwargs:
        """
        self.name = name
        self.profile = kwargs
        self.neighbors = {}
        self.status = status

    def get_status(self) -> int:
        """
        Return the status of the agent

        :return:
        """
        return self.status

    def set_status(self, status: float):
        """
        Set the status of the agent

        :param status:
        :return:
        """
        self.status = status

    def __str__(self) -> str:
        """
        Return a string representation of the Profile object.
        """
        return f"Name: {self.name}"

    def __dict__(self) -> dict:
        """
        Return a dictionary representation of the Profile object.
        """
        return {"name": self.name, **self.profile}

    def add_neighbor(self, neighbor: object):
        """
        Add a neighbor to the agent

        :param neighbor:
        :return:
        """
        self.neighbors[neighbor.name] = neighbor

    def add_neighbors(self, neighbors: list):
        """
        Add a list of neighbors to the agent

        :param neighbors:
        :return:
        """
        for neighbor in neighbors:
            self.add_neighbor(neighbor)

    def get_neighbor(self, name: str) -> object:
        """
        Get a neighbor by name

        :param name:
        :return:
        """
        return self.neighbors[name]

    def get_random_neighbor(self) -> object:
        """
        Get a random neighbor
        
        :return: 
        """
        return random.choice(list(self.neighbors.values()))

    def get_neighbors(self) -> list:
        """
        Get all the neighbors of the agent
        
        :return: 
        """
        return list(self.neighbors.values())

    def neighbors_iter(self) -> object:
        """
        Iterate over the neighbors of the agent
        
        :return: 
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

        :param agent:
        :return:
        """
        self.agents[agent.name] = agent

    def get_agent(self, name: str) -> object:
        """
        Get an agent by name
        
        :param name: 
        :return: 
        """
        return self.agents[name]

    def add_agents(self, agents: list):
        """
        Add a list of agents to the Agents object

        :param agents:
        :return:
        """
        for agent in agents:
            self.add_agent(agent)

    def get_random_agent(self) -> object:
        """
        Get a random agent
        
        :return: 
        """
        return random.choice(list(self.agents.values()))

    def agents_iter(self) -> object:
        """
        Iterate over the agents
        
        :return: 
        """
        for k, v in self.agents.items():
            yield k, v
