from llm_network.viz import OpinionEvolution, OpinionTrends, ShiftMatrix
import os.path


#for i in range(3):
#    for m in ['llama3', 'mistral']:
#        for c in ["same", "different"]:
#            filename = f"results/theseus_{c}_{m}_{i}.jsonl"
#            if os.path.exists(filename):
#                img = OpinionTrends(filename)
#                img.plot(f"trends/theseus_{c}_{m}_{i}_balanced.png")


for m in ["llama3", "mistral"]:
    for c in ["same", "different"]:
        filename = f"results/theseus_{c}_{m}_polarized_shifts.json"
        matr = ShiftMatrix(filename)
        matr.plot(f"trends/theseus_accept_{c}_{m}_polarized.png", "accept")
        matr.plot(f"trends/theseus_reject_{c}_{m}_polarized.png", "reject")
