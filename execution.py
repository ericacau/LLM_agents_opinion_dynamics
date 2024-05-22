from llm_network.simulator import LLMOpinionSimulator
import llm_network as llmn
import json

if __name__ == "__main__":
    # Simple example

    # Create a configuration
    config_list = {"llama3": {
            "model": "llama3",  # "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "api_base": "http://127.0.0.1:11434/v1",  # 8000
            "api_type": "open_ai",
            "api_key": "NULL",
        },

        "mistral": {
            "model": "mistral",  # "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "api_base": "http://127.0.0.1:11434/v1",  # 8000
            "api_type": "open_ai",
            "api_key": "NULL",
        }
    }

    llm_config = {
        "config_list": None,
        "seed": 42,
        "request_timeout": 1200,
        "max_tokens": -1,  # max response length, -1 no limits. Imposing limits may lead to truncated responses
        "temperature": 0.9,
    }

   # theme = ["Climate Change is a Hoax", "Global Warming is not real",
   #          "Humans are not the main producers of CO2", "Climate Change is natural and normal",
   #          "Plants and animals can adapt to climate change",
   #          "Climate Change is good for us",
   #          "Maybe Climate Change is real but there is nothing to be done, it's too late"]

    theme = ["""Theseus set sail to reclaim the throne as king of Athens. During the journey, parts of Theseus's ship began to break or decay; 
                Theseus and his crew replaced these parts as they sailed. Eventually, each part of the ship is replaced. 
                In the end the Ship of Theseus is still the same ship on which he originally sailed."""]
            #["Mountains are better than the seaside", "Going to the seaside is lame",
            # "Skying is better than swimming", "A cold winter is better than a hot summer",
            # ]

    # Create a network of agents from files
    net = llmn.Network()
    net.add_agents(
        "sample_data/agents_100_llm.json"
    )  # "../sample_data/example_agents.json"

    # g = nx.read_edgelist("../sample_data/example_net.csv", delimiter=",", nodetype=str)
    # net.set_network(g)

    # Create a dictionary with the instructions for each agent (not mandatory)
    instructions = json.load(
        open("sample_data/agents_instructions_no_neutral_output_v2.json")
    )  # "../sample_data/agents_instructions_theory_of_mind.json"
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
        n_iterations=1000,
        themes=theme,
        output_file="sample_data/Theseus_llama3.jsonl",
    )