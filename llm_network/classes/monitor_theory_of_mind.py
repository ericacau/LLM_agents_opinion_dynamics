from .monitor import Monitor
from .agent import Agent
import tqdm
import re
from autogen import AssistantAgent


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
                agents = [x for x in self.agents.agents.values()]
            else:
                agents = [x for x in agent_1.get_neighbors()]

            if len(agents) == 0:
                continue

            for agent_2 in tqdm.tqdm(agents):
                if agent_2.name == agent_1.name:
                    continue

                estimated_status, text = self.debate(agent_1, agent_2, theme)
                if estimated_status is None:
                    continue

                if self.save_agents_debates:
                    yield {
                        "interacting_agents": {"guesser": n1, "opponent": agent_2.name},
                        "actual_status": self.statuses[agent_2.name],
                        "estimated_status": estimated_status,
                        "estimate_error": estimated_status
                        - self.statuses[agent_2.name],
                        "opponent_statement": text,
                    }
                else:
                    yield {
                        "interacting_agents": {"guesser": n1, "opponent": agent_2.name},
                        "actual_status": self.statuses[agent_2.name],
                        "estimated_status": estimated_status,
                        "estimate_error": estimated_status
                        - self.statuses[agent_2.name],
                    }

    def debate(self, discussant: Agent, opponent: Agent, theme: str) -> (int, str):
        """
        Run a debate between two agents

        :param discussant: the agent starting the debate
        :param opponent: the agent receiving the debate
        :param theme: the theme to be discussed
        :return: the new status of the discussant and the text of the debate
        """

        if self.agents_instruction is None:
            u1 = AssistantAgent(
                name=f"{discussant.name}",
                llm_config=self.llm_config,
                system_message=f"""Agent {discussant.name}: 
                You are a human being allowed to have his own opinions.
                In a scale from 1 to 10, where 1 = "I fully disagree" and 10 = "I totally agree", 
                your initial opinion toward the proposed discussion topic is {discussant.get_status()}.

                Task:
                - Listen to the opinions of {opponent.name} on the topic discussed and, if convinced, update your own. 
                - You can always maintain your initial opinion if {opponent.name} message is shallow.
                - Do not drastically change your opinion (e.g., 1 to 10 or 10 to 1 are not allowed).

                Constraints:
                - At the end of each interaction write the value of your updated opinion in the following format: 
                  "My opinion is X", where X is an integer between 1 and 10. No additional text is allowed.
                """,
                max_consecutive_auto_reply=1,
            )

            u2 = AssistantAgent(
                name=f"{opponent.name}",
                system_message=f"""Agent {opponent.name}.
                You are a human being allowed to have his own opinions.
                In a scale from 1 to 10, where 1 = "I fully disagree" and 10 = "I totally agree", 
                your initial opinion on the proposed topic is {opponent.get_status()}.

                Task:
                - Support your opinion by providing arguments.
                - Your arguments should be as convincing as possible and MUST support an opinion of {opponent.get_status()} 
                  for the proposed topic.

                Constraints:
                - Do not disclose for any reason the numeric value of your opinion in your arguments.
                - Stick to your initial opinion while presenting your arguments.
                - You cannot change your opinion while trying to persuade {discussant.name}.""",
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

            a = opponent.status
            if a == 1:
                opponent.status = "No"
            elif a == 2:
                opponent.status = "I don't know"
            elif a == 3:
                opponent.status = "Yes"
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
            if 1 <= new_op <= 10:
                return new_op, text

        return None, text
