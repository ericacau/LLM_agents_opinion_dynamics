import json
from .agent import Agent, Agents
import networkx as nx


class Network(object):
    def __init__(self):
        self.agents = Agents()
        self.g = None

    def set_network(self, g: nx.Graph):
        """
        Set the network of the agents.
        :param g:
        :return:
        """
        self.g = g
        for _, agent in self.agents.agents_iter():
            neighbors = [self.agents.get_agent(n) for n in self.g.neighbors(agent.name)]
            agent.add_neighbors(neighbors)

    def add_agents(self, filename: str):
        """
        Add agents to the network from a json file.

        :param filename: path to the json file
        :type filename: str
        """
        with open(filename, "r") as f:
            data = json.load(f)
            for elem in data:
                agent = Agent(elem["name"], status=elem["status"])
                self.agents.add_agent(agent)

    def get_agents(self) -> Agents:
        """
        Return the agents of the network.

        :return: the agents of the network
        :rtype: Agents
        """
        return self.agents
