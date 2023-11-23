from .monitor import Monitor
import tqdm


class MonitorTheoryOfMind(Monitor):
    def iteration(self, theme: str) -> object:
        """
        Run an iteration of the simulation.
        Agents are selected randomly, but only those whose current status is within the epsilon range are considered.

        :param theme: theme to be discussed
        :return: a dictionary with the results of the iteration
        """
        for n1, agent_1 in self.agents.agents_iter():

            if self.meanfield:
                agents = [
                    x
                    for x in self.agents.agents.values()
                ]
            else:
                agents = [
                    x
                    for x in agent_1.get_neighbors()
                ]

            if len(agents) == 0:
                continue

            for agent_2 in tqdm.tqdm(agents):
                if agent_2.name == agent_1.name:
                    continue

                estimated_status, text = self.debate(agent_1, agent_2, theme)

                if self.save_agents_debates:
                    yield {
                        "interacting_agents": {"guesser": n1, "opponent": agent_2.name},
                        "actual_status": self.statuses[agent_2.name],
                        "estimated_status": estimated_status,
                        "estimate_error": estimated_status - self.statuses[agent_2.name],
                        "opponent_statement": text,
                    }
                else:
                    yield {
                        "interacting_agents": {"guesser": n1, "opponent": agent_2.name},
                        "actual_status": self.statuses[agent_2.name],
                        "estimated_status": estimated_status,
                        "estimate_error": estimated_status - self.statuses[agent_2.name],
                    }
