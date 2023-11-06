from .agent import Agent, Agents
from autogen import AssistantAgent
import re
import tqdm


class Monitor(object):
    def __init__(
        self, llm_config: dict, verbose: bool = False, save_agents_debates: bool = False
    ):
        """
        LLM Opinion Simulator

        :param llm_config: endpoint configuration
        :param verbose: whether to print or not the LLM output
        :param save_agents_debates: whether to save the debates of the agents
        """
        self.agents = None
        self.statuses = {}
        self.llm_config = llm_config
        self.verbose = verbose
        self.save_agents_debates = save_agents_debates

    def get_statuses(self) -> dict:
        """
        Get the statuses of the agents

        :return: the statuses of the agents
        """
        return self.statuses

    def set_agents(self, agents: Agents):
        """
        Set the agents in the monitor

        :param agents: a list of Agent objects
        :return:
        """
        self.agents = agents
        for name, agent in self.agents.agents_iter():
            self.statuses[name] = agent.get_status()

    def iteration(self, theme: str) -> object:
        """
        Run an iteration of the simulation

        :param theme: theme to be discussed
        :return: a dictionary with the results of the iteration
        """
        for n1, agent_1 in self.agents.agents_iter():
            agent_2 = agent_1.get_random_neighbor()
            new_status, text = self.debate(agent_1, agent_2, theme)

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

    def iteration_bunch(self, n: int, themes: object) -> object:
        """
        Run a bunch of iterations

        :param n: number of iterations, each involving a debate for each agent in the network
        :param themes: themes to be discussed
        :return: a generator of dictionaries with the results of the iterations
        """
        for i in tqdm.tqdm(range(n)):
            if isinstance(themes, str):
                yield self.iteration(themes)
            else:
                yield self.iteration(themes[i % len(themes)])

    def debate(self, agent_1: Agent, agent_2: Agent, theme: str) -> (int, str):
        """
        Run a debate between two agents

        :param agent_1:
        :param agent_2:
        :param theme:
        :return:
        """
        u1 = AssistantAgent(
            name=f"{agent_1.name}",
            llm_config=self.llm_config,
            system_message=f"""Agent {agent_1.name}: 
            You are a human being allowed to have his own opinions.
            In a scale from 1 to 10, where 1 = "I fully disagree" and 10 = "I totally agree", your initial opinion toward the proposed discussion topic is {agent_1.get_status()}.
            
            Task:
            - Listen to the opinions of {agent_2.name} on the topic discussed and, if convinced, update your own. 
            - You can always maintain your initial opinion if {agent_2.name} message is shallow.
            - Do not drastically change your opinion (e.g., 1 to 10 or 10 to 1 are not allowed).
            
            Constraints:
            - At the end of each interaction write the value of your updated opinion in the following format: "My opinion is X", where X is an integer between 1 and 10. No additional text is allowed.
            """,
            max_consecutive_auto_reply=1,
        )

        u2 = AssistantAgent(
            name=f"{agent_2.name}",
            system_message=f"""Agent {agent_2.name}.
            You are a human being allowed to have his own opinions.
            In a scale from 1 to 10, where 1 = "I fully disagree" and 10 = "I totally agree", your initial opinion on the proposed topic is {agent_2.get_status()}.
            
            Task:
            - Support your opinion by providing arguments.
            - Your arguments should be as convincing as possible and MUST support an opinion of {agent_2.get_status()} for the proposed topic.
                
            Constraints:
            - Do not disclose for any reason the numeric value of your opinion in your arguments.
            - Stick to your initial opinion while presenting your arguments.
            - You cannot change your opinion while trying to persuade {agent_1.name}.""",
            llm_config=self.llm_config,
            max_consecutive_auto_reply=1,
        )

        u1.initiate_chat(
            u2,
            message=f""" What do you think of the following statement?: "{theme}" """,
            silent=not self.verbose,  # default is False
            max_round=3,  # default is 3
        )

        final_text = u1.chat_messages[u2][-1]["content"]

        text = None
        if self.save_agents_debates:
            text = u1.chat_messages[u2][1]["content"]

        nb = re.findall(r"[0-9]+", final_text)

        if len(nb) > 0:
            return int(nb[-1]), text
        else:
            return agent_1.get_status(), text
