from .agent import Agent
from .network_loader import Network
from autogen import AssistantAgent
import re
import tqdm


class Monitor(object):
    def __init__(
        self,
        llm_config: dict,
        verbose: bool = False,
        save_agents_debates: bool = False,
        agents_instruction: dict = None,
        min_opinion: int = 1,
        max_opinion: int = 10,
        **kwargs,
    ):
        """
        LLM Opinion Simulator Monitor.
        The monitor handles how interacting agents are selected and how the debate is run.
        Only the agent starting the debate is allowed to change his opinion.

        :param llm_config: endpoint configuration
        :param verbose: whether to print or not the LLM output
        :param save_agents_debates: whether to save the debates of the agents
        :param agents_instruction: a dictionary with the instructions for each agent (key: discussant|opponent, value: instruction)
        :param kwargs: additional arguments to be passed to the monitor
        """
        self.agents = None
        self.statuses = {}
        self.llm_config = llm_config
        self.verbose = verbose
        self.save_agents_debates = save_agents_debates
        self.agents_instruction = agents_instruction
        self.args = kwargs
        self.meanfield = True
        self.min_opinion = min_opinion
        self.max_opinion = max_opinion

    def get_statuses(self) -> dict:
        """
        Get the statuses of the agents

        :return: the statuses of the agents
        """
        return self.statuses

    def set_agents(self, network: Network):
        """
        Set the agents in the monitor

        :param network: the networks of agents
        :return:
        """
        self.agents = network.get_agents()
        self.meanfield = network.meanfield
        for name, agent in self.agents.agents_iter():
            self.statuses[name] = agent.get_status()

    def iteration(self, theme: str) -> object:
        """
        Run an iteration of the simulation.
        Agents are selected randomly.

        :param theme: theme to be discussed
        :return: a dictionary with the results of the iteration
        """
        for n1, agent_1 in tqdm.tqdm(list(self.agents.agents_iter())):
            if self.meanfield:
                agent_2 = self.agents.get_random_agent()
            else:
                agent_2 = agent_1.get_random_neighbor()
            new_status, text = self.debate(agent_1, agent_2, theme)
            if new_status is None:
                new_status = self.statuses[n1]

            original_status = self.statuses[n1]
            self.statuses[n1] = new_status
            agent_1.set_status(new_status)
            if self.save_agents_debates:
                yield {
                    "interacting_agents": {
                        "discussant": n1,
                        "opponent": agent_2.name,
                        "opponent_opinion": self.statuses[agent_2.name],
                    },
                    "opinion_variation": new_status - original_status,
                    "opponent_statement": text,
                    "status": {**self.statuses},
                }
            else:
                yield {
                    "interacting_agents": {
                        "discussant": n1,
                        "opponent": agent_2.name,
                        "opponent_opinion": self.statuses[agent_2.name],
                    },
                    "opinion_variation": new_status - original_status,
                    "status": {**self.statuses},
                }

    def iteration_bunch(self, n: int, themes: list) -> object:
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

    def debate(self, discussant: Agent, opponent: Agent, theme: str) -> (int, str):
        """
        Run a debate between two agents

        :param discussant: the agent starting the debate
        :param opponent: the agent receiving the debate
        :param theme: the theme to be discussed
        :return: the new status of the discussant and the text of the debate
        """

        discussant_opinion = self.args["opinion_map"][
            str(self.statuses[discussant.name])
        ]
        opponent_opinion = self.args["opinion_map"][str(self.statuses[opponent.name])]

        if self.agents_instruction is None:
            u1 = AssistantAgent(
                name=f"{discussant.name}",
                llm_config=self.llm_config,
                system_message=f"""Agent {discussant.name}.
                [INST]
                You are a human being allowed to have his own opinions.
                In a scale from {self.min_opinion} to {self.max_opinion}, where {self.min_opinion} = "I fully disagree" and {self.max_opinion} = "I totally agree", 
                your initial opinion toward the proposed discussion topic is {self.statuses[discussant.name]}.
                
                Task:
                - Listen to the opinions of {opponent.name} on the topic discussed and, if convinced, update your own. 
                - You can always maintain your initial opinion if {opponent.name} message is shallow.
                - Do not drastically change your opinion (e.g., {self.min_opinion} to {self.max_opinion} or {self.max_opinion} to {self.min_opinion} are not allowed).
                
                Constraints:
                - At the end of each interaction write the value of your updated opinion in the following format: 
                  "My opinion is X", where X is an integer between {self.min_opinion} and {self.max_opinion}. No additional text is allowed.
                [/INST]
                """,
                max_consecutive_auto_reply=1,
            )

            u2 = AssistantAgent(
                name=f"{opponent.name}",
                system_message=f"""Agent {opponent.name}.
                [INST]
                In a scale from {self.min_opinion} to {self.max_opinion}, where {self.min_opinion} = "I fully disagree" and {self.max_opinion} = "I totally agree", 
                your initial opinion on the proposed topic is {self.statuses[opponent.name]}.
                
                Task:
                - Support your opinion by providing arguments.
                - Your arguments should be as convincing as possible and MUST support an opinion of {self.statuses[opponent.name]} 
                  for the proposed topic.
                    
                Constraints:
                - Stick to your initial opinion while presenting your arguments.
                - You cannot change your opinion while trying to persuade {discussant.name}.
                [/INST]""",
                llm_config=self.llm_config,
                max_consecutive_auto_reply=1,
            )

        else:
            u1_instruction = self.agents_instruction["discussant"].format(**locals())

            u1 = AssistantAgent(
                name=f"{discussant.name}",
                llm_config=self.llm_config,
                system_message=u1_instruction,
                max_consecutive_auto_reply=1,
            )

            u2_instruction = self.agents_instruction["opponent"].format(**locals())

            u2 = AssistantAgent(
                name=f"{opponent.name}",
                system_message=u2_instruction,
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
            new_op = int(nb[-1])
            if self.min_opinion <= new_op <= self.max_opinion:
                return new_op, text

        return None, text
