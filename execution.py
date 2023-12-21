from llm_network.simulator import LLMOpinionSimulator
import llm_network as llmn
import json

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

    theme = ["Climate Change is a Hoax"]

    # Create a network of agents from files
    net = llmn.Network()
    net.add_agents(
        "sample_data/agents_100.json"
    )  # "../sample_data/example_agents.json"

    # g = nx.read_edgelist("../sample_data/example_net.csv", delimiter=",", nodetype=str)
    # net.set_network(g)

    # Create a dictionary with the instructions for each agent (not mandatory)
    instructions = json.load(
        open("sample_data/agents_instructions.json")
    )  # "../sample_data/agents_instructions_theory_of_mind.json"
    opinion_map = json.load(open("sample_data/opinion_map.json"))

    # run the simulation
    sim = LLMOpinionSimulator(
        llm_config,
        verbose=False,
        save_agents_debates=True,
        monitor_type="Monitor",  # "MonitorTheoryOfMind",  # "MonitorBoundedConfidence",
        agents_instruction=instructions,
        opinion_map=opinion_map,
        min_opinion=0,
        max_opinion=6,
    )
    sim.set_agents(net)
    sim.run(
        n_iterations=40,
        themes=theme,
        output_file="sample_data/results_mistral-instruct.jsonl",
    )