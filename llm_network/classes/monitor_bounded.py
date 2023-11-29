from .monitor import Monitor
import random


class MonitorBoundedConfidence(Monitor):
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
                    if max([1, (agent_1.status - agent_1.args["epsilon"])])
                    <= x.status
                    <= min([10, (agent_1.status + agent_1.args["epsilon"])])
                ]
            else:
                agents = [
                    x
                    for x in agent_1.get_neighbors()
                    if max([1, (agent_1.status - agent_1.args["epsilon"])])
                    <= x.status
                    <= min([10, (agent_1.status + agent_1.args["epsilon"])])
                ]

            if len(agents) == 0:
                continue

            agent_2 = random.choice(agents)

            new_status, text = self.debate(agent_1, agent_2, theme)
            if new_status is None:
                new_status = self.statuses[n1]

            original_status = self.statuses[n1]
            self.statuses[n1] = new_status
            agent_1.set_status(new_status)
            if self.save_agents_debates:
                yield {
                    "status": {**self.statuses},
                    "interacting_agents": {"discussant": n1, "opponent": agent_2.name},
                    "opinion_variation": new_status - original_status,
                    "opponent_statement": text,
                }
            else:
                yield {
                    "status": {**self.statuses},
                    "interacting_agents": {"discussant": n1, "opponent": agent_2.name},
                    "opinion_variation": new_status - original_status,
                }
