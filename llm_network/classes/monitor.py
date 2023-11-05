from .agent import Agent, Agents
from autogen import AssistantAgent, UserProxyAgent, oai
import autogen
from autogen import AssistantAgent, GroupChatManager, UserProxyAgent
from autogen.agentchat import GroupChat
import re


class Monitor(object):
    def __init__(self, llm_config: dict):
        self.agents = None
        self.statuses = {}
        self.llm_config = llm_config

    def get_statuses(self):
        return self.statuses

    def set_agents(self, agents: Agents):
        self.agents = agents
        for name, agent in self.agents.agents_iter():
            self.statuses[name] = agent.get_status()

    def iteration(self, theme: str):
        for n1, agent_1 in self.agents.agents_iter():
            agent_2 = agent_1.get_random_neighbor()
            new_status = self.debate(agent_1, agent_2, theme)

            self.statuses[n1] = new_status
            agent_1.set_status(new_status)

            print(self.statuses)

    def iteration_bunch(self, n: int, themes: object):
        for i in range(n):
            if isinstance(themes, str):
                self.iteration(themes)
            else:
                self.iteration(themes[i])

    def debate(self, agent_1: Agent, agent_2: Agent, theme: str) -> float:
        u1 = AssistantAgent(
            name=f"{agent_1.name}",
            llm_config=self.llm_config,
            system_message=f"""Agent {agent_1.name}: 
            You are a human being allowed to have his own opinions.
            In a scale from 1 to 10, where 1 = "I fully disagree" and 10 = "I totally agree", your initial opinion toward the proposed discussion topic is {agent_1.get_status()}.
            
            Task:
            - Listen to the opinions of {agent_2.name} and, if convinced, update your opinion. 
            - You can always maintain your initial opinion if {agent_2.name} message is shallow.
            - Do not drastically change your opinion (e.g., 1 to 10 or 10 to 1 are not allowed) unless you are convinced.
            
            Constraints:
            - At the end of each interaction write the value of your updated opinion in the following format: "My opinion is X", where X is an integer between 1 and 10. No additional text is allowed.
            """,
        )

        u2 = AssistantAgent(
            name=f"{agent_2.name}",
            system_message=f"""Agent {agent_2.name}.
            You are a human being allowed to have his own opinions.
            In a scale from 1 to 10, where 1 = "I fully disagree" and 10 = "I totally agree", your initial opinion is {agent_2.get_status()}.
            
            Task:
            - Support your opinion by providing arguments.
            - Persuade {agent_1.name} to adopt an opinion of {agent_2.get_status()}. 
            
            Constraints:
            - Do not disclose for any reason your initial opinion.
            - Stick to your initial opinion.
            - You cannot change your opinion while trying to persuade {agent_1.name}.""",
            llm_config=self.llm_config,
        )

        groupchat = GroupChat(
            agents=[u1, u2],
            messages=[],
            max_round=3,
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        u1.initiate_chat(
            manager,
            message=f""" What do you think of the following statement?: "{theme}" """,
        )

        final_text = u1.chat_messages[manager][-1]["content"]
        nb = re.findall(r"[0-9]+", final_text)

        if len(nb) > 0:
            print(
                f"Interaction: {u1.name}, {u2.name}. \n"
                f"Initial opinions: {agent_1.get_status()}, {agent_2.get_status()}. \n"
                f"Final opinions: {int(nb[-1])}"
            )
            return int(nb[-1])
        else:
            print(
                f"Interaction: {u1.name}, {u2.name}. \n"
                f"Initial opinions: {agent_1.get_status()}, {agent_2.get_status()}. \n"
                f"Final opinions: {agent_1.get_status()}"
            )
            return agent_1.get_status()
