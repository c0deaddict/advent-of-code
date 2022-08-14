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


def find_vertices(input):
    return ((v, p) for (p, v) in input.items() if v not in ("#", "."))


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
    v, keys = node
    for u, dist in graph[v].items():
        if u == "@":
            yield dist, (u, keys)
        elif u.islower():
            yield dist, (u, keys | {u})
        elif u.lower() in keys:
            yield dist, (u, keys)


def path_dist(graph, path):
    dist = 0
    v = path[0]
    for u in path[1:]:
        dist += graph[v[0]][u[0]]
        v = u
    return dist


def part1(input):
    vertices = list(find_vertices(input))
    num_keys = sum(1 for v, _ in vertices if v.islower())
    entrance = dict(vertices)["@"]
    graph = scan_graph(input, entrance)

    start = ("@", frozenset())
    h = lambda node: num_keys - len(node[1])
    is_target = lambda node: len(node[1]) == num_keys
    path = astar(start, partial(adjacent, graph), h, is_target)
    return path_dist(graph, path)


def corners(point):
    x, y = point
    return [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]


def patch_map(input, entrance):
    input[entrance] = "#"
    for n in neighbours(entrance):
        input[n] = "#"
    entrances = corners(entrance)
    for e in entrances:
        input[e] = "@"
    return entrances


def adjacent_part2(graphs, node):
    bots, keys = node
    for i, v in enumerate(bots):
        for u, dist in graphs[i][v].items():
            new_bots = bots[:i] + (u,) + bots[i + 1 :]
            if u == "@":
                yield dist, (new_bots, keys)
            elif u.islower():
                yield dist, (new_bots, keys | {u})
            elif u.lower() in keys:
                yield dist, (new_bots, keys)


def path_dist_part2(graphs, path):
    dist = 0
    bots = list(path[0][0])
    for next in path[1:]:
        for i, (v, u) in enumerate(zip(bots, next[0])):
            if u != v:
                bots[i] = u
                dist += graphs[i][v][u]
    return dist


def part2(input):
    vertices = list(find_vertices(input))
    num_keys = sum(1 for v, _ in vertices if v.islower())

    # Patch map if it has a single entrance.
    entrances = [pos for (v, pos) in vertices if v == "@"]
    if len(entrances) == 1:
        entrances = patch_map(input, entrances[0])

    # Make a graph for each entrance.
    graphs = [scan_graph(input, e) for e in entrances]

    start = (tuple("@" for e in entrances), frozenset())
    h = lambda node: num_keys - len(node[1])
    is_target = lambda node: len(node[1]) == num_keys
    path = astar(start, partial(adjacent_part2, graphs), h, is_target)
    return path_dist_part2(graphs, path)


def main():
    with open("../input/day_18.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1_example1():
    input = """
#########
#b.A.@.a#
#########
"""
    assert part1(parse_input(input)) == 8


def test_part1_example2():
    input = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""
    assert part1(parse_input(input)) == 86


def test_part1_example3():
    input = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""
    assert part1(parse_input(input)) == 132


def test_part1_example4():
    input = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
    assert part1(parse_input(input)) == 136


def test_part1_example5():
    input = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""
    assert part1(parse_input(input)) == 81


def test_part2_example1():
    input = """
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
"""
    assert part2(parse_input(input)) == 8


def test_part2_example2():
    input = """
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
"""
    assert part2(parse_input(input)) == 24


def test_part2_example3():
    input = """
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
"""
    assert part2(parse_input(input)) == 32


def test_part2_example4():
    input = """
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
"""
    assert part2(parse_input(input)) == 72
