from llm_network.classes import Agent, Agents, Monitor

config_list = [
    {
        "model": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        "api_base": "http://127.0.0.1:8000/v1",
        "api_type": "open_ai",
        "api_key": "NULL",
    }
]

llm_config = {"config_list": config_list, "seed": 42, "request_timeout": 1200,}

a1 = Agent(name="a1", status=5, age=30)
a2 = Agent(name="a2", status=6, age=14)
a3 = Agent(name="a3", status=8, age=37)
a4 = Agent(name="a4", status=1, age=75)

a1.add_neighbors([a2, a3])
a2.add_neighbors([a1, a4])
a3.add_neighbors([a1, a4])
a4.add_neighbors([a2, a3])

agents = Agents()
agents.add_agents([a1, a2, a3, a4])

monitor = Monitor(llm_config)
monitor.set_agents(agents)

monitor.iteration_bunch(10, "Gun control is a good idea.")