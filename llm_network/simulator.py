import networkx as nx

import llm_network.classes as llmn
import json


class LLMOpinionSimulator(object):
    def __init__(
        self,
        llm_config: dict,
        config_list: dict,
        verbose: bool = False,
        save_agents_debates: bool = False,
        monitor_type: str = "Monitor",
        agents_instruction: dict = None,
        opinion_map: dict = None,
        min_opinion: int = 1,
        max_opinion: int = 10,
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
            config_list,
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

