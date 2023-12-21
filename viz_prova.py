from llm_network.viz import OpinionEvolution


filename = "sample_data/results_mistral-instruct.jsonl"

img = OpinionEvolution(filename)
img.plot("viz.png")