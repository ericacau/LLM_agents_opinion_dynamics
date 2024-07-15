import json


res = []
model = "mistral"

with open(f"agents_polarized_140_llm_{model}.json", "w") as o:
    ags = json.load(open("agents_polarized_140.json"))
    for l in ags:
        if int(l["name"][1:]) % 2 == 0:
            l["llm_name"] = model
        else:
            l["llm_name"] = model

        res.append(l)

    o.write(json.dumps(res) + "\n")
