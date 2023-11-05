from llm_network.classes import Agent, Agents, Monitor
import json


class LLMOpinionSimulator(object):
    def __init__(
        self, llm_config: dict, verbose: bool = False, save_agents_debates: bool = False
    ):
        self.monitor = Monitor(
            llm_config, verbose=False, save_agents_debates=save_agents_debates
        )
        self.statuses = {}
        self.llm_config = llm_config
        self.verbose = verbose

    def set_agents(self, agents: Agents):
        self.monitor.set_agents(agents)

    def run(
        self, n_iterations: int, themes: object, output_file: str = "results.jsonl"
    ):
        with open(output_file, "w") as f:
            f.write(f"{json.dumps(self.monitor.statuses)}\n")
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
            "model": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "api_base": "http://127.0.0.1:8000/v1",
            "api_type": "open_ai",
            "api_key": "NULL",
        }
    ]

    llm_config = {
        "config_list": config_list,
        "seed": 42,
        "request_timeout": 1200,
    }

    theme = "'Big Data' is only an empty buzz word."

    # Create agents
    a1 = Agent(name="a1", status=9)
    a2 = Agent(name="a2", status=3)
    a3 = Agent(name="a3", status=7)
    a4 = Agent(name="a4", status=1)

    # create network
    a1.add_neighbors([a2, a3])
    a2.add_neighbors([a1, a4])
    a3.add_neighbors([a1, a4])
    a4.add_neighbors([a2, a3])

    # prepare agents set
    agents = Agents()
    agents.add_agents([a1, a2, a3, a4])

    # run the simulation
    sim = LLMOpinionSimulator(llm_config, verbose=False, save_agents_debates=True)
    sim.set_agents(agents)
    sim.run(n_iterations=10, themes=theme, output_file="results.jsonl")
