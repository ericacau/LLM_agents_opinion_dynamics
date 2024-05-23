from llm_network.viz import OpinionEvolution, OpinionTrends

filename = "results/old/Theseus_mistral_run1_backfire.jsonl"

img = OpinionTrends(filename)
img.plot("Theseus_mistral_run1.png")
