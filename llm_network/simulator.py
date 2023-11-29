import networkx as nx

import llm_network.classes as llmn
import json


class LLMOpinionSimulator(object):
    def __init__(
        self,
        llm_config: dict,
        verbose: bool = False,
        save_agents_debates: bool = False,
        monitor_type: str = "Monitor",
        agents_instruction: dict = None,
        opinion_map: dict = None,
        min_opinion: int = 1,
        max_opinion: int = 10
    ):
        """
        LLM Opinion Simulator

        :param llm_config: endpoint configuration
        :param verbose: whether to print or not the LLM output
        :param save_agents_debates: whether to save the debates of the agents
        :param monitor_type: type of monitor to be used (e.g., Monitor, MonitorBoundedConfidence)
        :param agents_instruction: a dictionary with the instructions for each agent (key: discussant|opponent, value: instruction)
        """

        monitor = getattr(llmn, monitor_type)

        self.monitor = monitor(
            llm_config,
            verbose=False,
            save_agents_debates=save_agents_debates,
            agents_instruction=agents_instruction,
            opinion_map=opinion_map,
            min_opinion=min_opinion,
            max_opinion=max_opinion,
        )
        self.statuses = {}
        self.llm_config = llm_config
        self.verbose = verbose

    def set_agents(self, network: llmn.Network):
        """
        Set the agents in the monitor

        :param network: network of agents
        """
        self.monitor.set_agents(network)

    def run(
        self, n_iterations: int, themes: object, output_file: str = "results.jsonl"
    ):
        """
        Run the simulation

        :param n_iterations: number of iterations
        :param themes: themes to be discussed
        :param output_file: output file
        """
        with open(output_file, "w") as f:
            initial_statuses = {"status": self.monitor.statuses}
            f.write(f"{json.dumps(initial_statuses)}\n")
            iterations = self.monitor.iteration_bunch(n_iterations, themes=themes)
            for it in iterations:
                for i in it:
                    f.write(f"{json.dumps(i)}\n")
                    f.flush()


if __name__ == "__main__":
    # Simple example

    # Create a configuration
    config_list = [
        {
            "model": "mistral-7bclear-instruct-v0.1.Q4_K_M.gguf",
            "api_base": "http://10.8.0.1:8081/v1",
            "api_type": "open_ai",
            "api_key": "NULL",
        }
    ]

    llm_config = {
        "config_list": config_list,
        "seed": 42,
        "request_timeout": 1200,
        "max_tokens": -1,  # max response length, -1 no limits. Imposing limits may lead to truncated responses
        "temperature": 0.9,
    }

    theme = ["Luck is a matter of preparation"]

    # Create a network of agents from files
    net = llmn.Network()
    net.add_agents("../sample_data/agents_100.json")  # "../sample_data/example_agents.json"

    # g = nx.read_edgelist("../sample_data/example_net.csv", delimiter=",", nodetype=str)
    # net.set_network(g)

    # Create a dictionary with the instructions for each agent (not mandatory)
    instructions = json.load(
        open("../sample_data/agents_instructions.json")
    )  # "../sample_data/agents_instructions_theory_of_mind.json"
    opinion_map = json.load(open("../sample_data/opinion_map.json"))

    # run the simulation
    sim = LLMOpinionSimulator(
        llm_config,
        verbose=False,
        save_agents_debates=True,
        monitor_type="Monitor",  # "MonitorTheoryOfMind",  # "MonitorBoundedConfidence",
        agents_instruction=instructions,
        opinion_map=opinion_map,
        min_opinion=0,
        max_opinion=6
    )
    sim.set_agents(net)
    sim.run(
        n_iterations=10,
        themes=theme,
        output_file="../sample_data/results_mistral-instruct.jsonl",
    )
