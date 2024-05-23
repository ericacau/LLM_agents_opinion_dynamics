import json


res = []

with open("agents_140_llm_llama3.json", "w") as o:

    ags = json.load(open("agents_140.json"))
    for l in ags:

        if int(l["name"][1:]) % 2 == 0:
            l["llm_name"] = "llama3"
        else:
            l["llm_name"] = "llama3"

        res.append(l)

    o.write(json.dumps(res) + "\n")