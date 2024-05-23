from llm_network.simulator import LLMOpinionSimulator
import llm_network as llmn
import json
import sys
import os


def execute(model, config_list, theme, network, n, name):
    llm_config = {
        "config_list": None,
        "seed": 42,
        "request_timeout": 1200,
        "max_tokens": -1,  # max response length, -1 no limits. Imposing limits may lead to truncated responses
        "temperature": 0.9,
    }

    print(os.getcwd())
    # Create a network of agents from files
    net = llmn.Network()
    net.add_agents(
        f"sample_data/agents_140_llm_{model}.json"
    )

    if network is not None:
        net.set_network(g)

    # Create a dictionary with the instructions for each agent (not mandatory)
    instructions = json.load(
        open("sample_data/agents_instructions_Theseus.json")
    )
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
        output_file=f"results/{name}_{model}_{n}.jsonl",
    )


if __name__ == "__main__":
    # Simple example

    model = sys.argv[1]
    run_n = int(sys.argv[2])
    theme_name = sys.argv[3]
    try:
        network = sys.argv[4]
    except IndexError:
        network = None

    # Create a configuration
    config_list = {
        f"{model}": {
            "model": f"{model}",  # "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "api_base": "http://127.0.0.1:11434/v1",  # 8000
            "api_type": "open_ai",
            "api_key": "NULL",
        }
    }

    theme = json.load(open(f"themes/{theme_name}", "r"))

    if network is not None:
        network = nx.read_edgelist(f"networks/{network}", delimiter=",", nodetype=str)


    for n in range(run_n):
        execute(model, config_list, theme, network, n, theme_name)


