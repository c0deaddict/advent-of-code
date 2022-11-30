import pytest
from collections import namedtuple
import operator
from functools import partial
from operator import itemgetter
from itertools import chain, count

from astar import astar


def parse_input(input):
    return dict(
        ((x, y), ch)
        for (y, line) in enumerate(input.strip().splitlines())
        for (x, ch) in enumerate(line.strip())
    )


def neighbours(point):
    x, y = point
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def print_map(input):
    points = input.keys()
    minx = min(points, key=itemgetter(0))[0]
    miny = min(points, key=itemgetter(1))[1]
    maxx = max(points, key=itemgetter(0))[0]
    maxy = max(points, key=itemgetter(1))[1]

    for y in range(miny, maxy + 1):
        print("".join(input[(x, y)] for x in range(minx, maxx + 1)))


def find_points(input):
    return ((v, p) for (p, v) in input.items() if v.isdigit())


def scan(input, start):
    frontier = set([start])
    visited = set([start])
    edges = []
    for dist in count(start=1):
        frontier = set(
            n
            for n in chain(*(neighbours(p) for p in frontier))
            if input.get(n) != "#" and n not in visited
        )
        if len(frontier) == 0:
            return edges

        visited.update(frontier)

        for p in list(frontier):
            if input[p] != ".":
                edges.append((p, dist))
                frontier.remove(p)


def scan_graph(input, start):
    graph = {}
    queue = [start]
    visited = set()
    while queue:
        pos = queue.pop()
        v = input[pos]
        graph[v] = {}
        for p, dist in scan(input, pos):
            u = input[p]
            graph[v][u] = dist
            if u not in graph and p not in queue:
                queue.append(p)
    return graph


def adjacent(graph, node):
    v, points = node
    for u, dist in graph[v].items():
        yield dist, (u, points + (u,))


def path_dist(graph, path):
    return sum(graph[v[0]][u[0]] for v, u in zip(path, path[1:]))


def part1(input):
    points = list(find_points(input))
    current = dict(points)["0"]
    graph = scan_graph(input, current)

    start = ("0", ("0",))
    h = lambda node: len(points) - len(set(node[1]))
    is_target = lambda node: len(set(node[1])) == len(points)
    path = astar(start, partial(adjacent, graph), h, is_target)
    return path_dist(graph, path)


def part2(input):
    points = list(find_points(input))
    current = dict(points)["0"]
    graph = scan_graph(input, current)

    start = ("0", ("0",))
    h = lambda node: (1 + len(points)) - (
        len(set(node[1])) + 1 if node[1][-1] == "0" else 0
    )
    is_target = lambda node: len(set(node[1])) == len(points) and node[1][-1] == "0"
    path = astar(start, partial(adjacent, graph), h, is_target)
    return path_dist(graph, path)


def main():
    with open("../input/day_24.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 14
