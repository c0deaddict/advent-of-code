import re
from itertools import chain


def parse_input(input):
    return [
        re.match(
            r"^Step ([A-Z]) must be finished before step ([A-Z]) can begin\.$", line
        ).groups()
        for line in input.strip().splitlines()
    ]


def dependency_graph(input):
    steps = set(chain(*input))
    return {k: set(a for (a, b) in input if b == k) for k in steps}


def part1(input):
    graph = dependency_graph(input)
    visited = set()
    result = []
    while len(graph):
        steps = [k for k, deps in graph.items() if deps.issubset(visited)]
        k = sorted(steps)[0]
        del graph[k]
        visited.add(k)
        result.append(k)
    return "".join(result)


def part2(input):
    pass


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def test_part1_example1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == "CABDFE"
