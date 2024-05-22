import json


res = []

with open("agents_100_llm_phi.json", "w") as o:

    ags = json.load(open("agents_100.json"))
    for l in ags:

        if int(l["name"][1:]) % 2 == 0:
            l["llm_name"] = "phi"
        else:
            l["llm_name"] = "phi3"

        res.append(l)

    o.write(json.dumps(res) + "\n")