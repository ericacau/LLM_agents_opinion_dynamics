from llm_network.simulator import LLMOpinionSimulator
import llm_network as llmn
import networkx as nx
import json
import sys


def execute(
    models,
    config_list,
    network,
    n,
    name,
    theme=None,
    theme_name="theseus",
    experiment="unbalanced",
    n_agents=140,
):
    llm_config = {
        "config_list": None,
        "seed": 42,
        "request_timeout": 1200,
        "max_tokens": -1,  # max response length, -1 no limits. Imposing limits may lead to truncated responses
        "temperature": 0.9,
    }

    # Create a network of agents from files
    net = llmn.Network()
    net.add_agents(f"sample_data/agents_{experiment}_{n_agents}_llm_{models}.json")

    if network is not None:
        g = nx.read_edgelist(f"sample_data/{network}", nodetype=str)
        net.set_network(g)

    # Create a dictionary with the instructions for each agent (not mandatory)
    instructions = json.load(open(f"sample_data/agents_instructions_{theme_name}.json"))
    opinion_map = json.load(open("sample_data/opinion_map.json"))

    # run the simulation
    sim = LLMOpinionSimulator(
        llm_config,
        config_list,
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
        n_iterations=100,
        themes=theme,
        output_file=f"results/{name.split('.')[0]}_{models}_{n}_{experiment}.jsonl",
    )


if __name__ == "__main__":
    # Simple example

    models = sys.argv[1]
    run_n = int(sys.argv[2])
    theme_name = sys.argv[3]
    exp_name = sys.argv[4]
    n_agents = int(sys.argv[5])
    try:
        network = sys.argv[6]
    except IndexError:
        network = None

    model_list = models.split(",")

    config_list = {}

    # Create a configuration for each model
    for model in model_list:
        config_list[model] = {
            "model": f"{model}",
            "api_base": "http://127.0.0.1:11434/v1",
            "api_type": "open_ai",
            "api_key": "NULL",
        }

    theme = json.load(open(f"themes/{theme_name}", "r"))

    if network is not None:
        network = nx.read_edgelist(f"networks/{network}", delimiter=",", nodetype=str)

    for n in range(run_n):
        execute(
            models=models,
            config_list=config_list,
            network=network,
            n=n,
            name=theme_name,
            theme=theme,
            experiment=exp_name,
            n_agents=n_agents,
        )
