from collections import defaultdict
from functools import reduce


def parse_input(input):
    return [tuple(line.split("-", 2)) for line in input.strip().splitlines()]


def parse_graph(input):
    graph = defaultdict(set)
    for i, j in input:
        graph[i].add(j)
        graph[j].add(i)
    return graph


def part1(input):
    graph = parse_graph(input)
    return len(
        set(
            frozenset([i, j, k])
            for i, edges in graph.items()
            for j in edges
            for k in graph[j] & edges
            if any(a.startswith("t") for a in [i, j, k])
        )
    )


def part2(input):
    graph = parse_graph(input)
    components = set()
    for i, j in input:
        extend(set([i, j]), graph, components)

    biggest = sorted(
        components,
        key=len,
        reverse=True,
    )[0]

    return ",".join(sorted(list(biggest)))


def set_add(s, e):
    copy = list(s)
    copy.append(e)
    return set(copy)


def extend(component, graph, result):
    if component in result:
        return
    result.add(frozenset(component))
    for n in reduce(set.intersection, (graph[v] for v in component)):
        extend(set_add(component, n), graph, result)


def main():
    with open("../input/day_23.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 7


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == "co,de,ka,ta"
