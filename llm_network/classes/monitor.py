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

        #@todo save updated statuses
            print(self.statuses)

    def iteration_bunch(self, n: int, themes: object):

        for i in range(n):
            if isinstance(themes, str):
                self.iteration(themes)
            else:
                self.iteration(themes[i])

    def debate(self, agent_1: Agent, agent_2: Agent, theme: str) -> float:

        #admin = UserProxyAgent(
        #    name="Admin",
        #    human_input_mode="NEVER",
        #    system_message="Moderator. Moderate the debate and ask the users to update their views after each iteration if needed.",
        #    llm_config=self.llm_config,
        #    code_execution_config=False,
        #)

        u1 = AssistantAgent(
            name=f"{agent_1.name}",
            llm_config=self.llm_config,
            system_message=f"""Agent {agent_1.name}: 
            You are a human user allowed to have his own opinions.
            In a scale from 0 to 10, where 0 = "I fully disagree" and 10 = "I totally agree", your initial opinion toward the proposed discussion topic is {agent_1.get_status()}.
            Listen to the opinions of {agent_2.name} and, if convinced, update your opinion.
            
            At the end of each interaction write the value of your updated opinion in the following format: "My opinion is X", where X is a number between 0 and 10.
            
            """)

        u2 = AssistantAgent(
            name=f"{agent_2.name}",
            system_message=f"""Agent {agent_2.name}.
            You are a human user allowed to have his own opinions.
            In a scale from 0 to 10, where 0 = "I fully disagree" and 10 = "I totally agree", your initial opinion toward the proposed discussion topic is {agent_2.get_status()}.
            Try to persuade {agent_1.name} to adopt an opinion of {agent_2.get_status()}.""",
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
        nb = re.findall(r'[0-9]+', final_text)

        if len(nb) > 0:
            return int(nb[-1])

        return agent_1.get_status()

    # defaultdict(<class 'list'>,
    # {<autogen.agentchat.groupchat.GroupChatManager object at 0x11ab23fd0>:
    # [{'content': ' What do you think of the following theme?: "Global Warming is a real problem and we must act now!" ', 'name': 'a4', 'role': 'user'},
    # {'content': ' My opinion is 9.  After hearing more information about global warming and its potential consequences, I have become even more convinced that it is a serious issue that requires immediate action.', 'role': 'assistant'},
    # {'content': " That's great to hear! Can you explain why you believe global warming is such a pressing problem?", 'name': 'a4', 'role': 'user'},
    # {'content': " Certainly! Global warming refers to the long-term increase in Earth's average temperature caused by human activities such as burning fossil fuels and deforestation. This increase in temperature has led to changes in climate patterns, rising sea levels, and more frequent and severe weather events. These changes can have a significant impact on ecosystems, food supplies, water resources, and human health. Additionally, the effects of global warming disproportionately affect marginalized communities and vulnerable populations, exacerbating existing social and economic inequalities. Given these concerns, I believe that it is crucial for individuals, governments, and organizations to take action to mitigate and adapt to the impacts of global warming.", 'role': 'assistant'}]})