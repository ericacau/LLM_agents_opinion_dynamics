import json

for m in ["llama3", "mistral"]:
    for c in ["same", "different"]:
        shifts = []
        for i in range(3):
            filename = f"results/theseus_{c}_{m}_{i}.jsonl"

            with open(filename, "r") as f:
                f.readline()
                for l in f:
                    try:
                        l = json.loads(l)

                        do = l["interacting_agents"]["discussant_opinion"]
                        oo = l["interacting_agents"]["opponent_opinion"]

                        dans = l["discussant_answer"].split()
                        res = ""
                        if "ACCEPT" in dans:
                            res = "accept"
                        elif "REJECT" in dans:
                            res = "reject"
                        else:
                            res = "none"

                        shifts.append((do, oo, res))
                    except:
                        pass

        with open(f"results/theseus_{c}_{m}_shifts.json", "w") as f:
            f.write(json.dumps(shifts))
