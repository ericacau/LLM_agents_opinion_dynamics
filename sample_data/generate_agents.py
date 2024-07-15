import json


def generate_agents(n=140, opinions=7):
    res = []

    b = int(n / opinions)
    current = 0
    op = 0
    for i in range(n):
        agent = {"name": f"a{i}", "status": op}
        current = current + 1

        if current >= b:
            op += 1
            current = 0

        res.append(agent)

    return res


def generate_unbalanced_agents(n=140, opinions=7):
    res = []

    b = int(n / opinions)
    current = 0
    op = 0
    for i in range(81):
        agent = {"name": f"a{i}", "status": 0}
        #current = current + 1

        #if current >= b:
        #    op += 1
        #    current = 0

        res.append(agent)

    for i in range(81, n):
        agent = {"name": f"a{i}", "status": op}
        current = current + 1

        if current >= b:
            op += 1
            current = 0

        res.append(agent)

    return res


def generate_polarized_agents(n=140, opinions=7):
    res = []

    for i in range(71):
        agent = {"name": f"a{i}", "status": 0}
        res.append(agent)

    for i in range(71, n):
        agent = {"name": f"a{i}", "status": 6}
        res.append(agent)

    return res


if __name__ == "__main__":
    n = 140
    agents = generate_polarized_agents(n=n, opinions=7)
    json.dump(agents, open(f"agents_polarized_{n}.json", "w"))
