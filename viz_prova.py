from llm_network.viz import OpinionEvolution, OpinionTrends

filename = "results/Theseus_llama3.jsonl"

img = OpinionTrends(filename)
img.plot("Theseus_llama3.png")


