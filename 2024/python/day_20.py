from collections import Counter
from itertools import count

from lib import Vector


def find_tile(input, tile):
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == tile:
                return Vector(x, y)
    assert False


def parse_input(input):
    return input.strip().splitlines()


def adjacent(input, node):
    return [
        (1, n) for n in node.neighbors() if n.in_area(input) and n.get(input) != "#"
    ]


def adjacent_cheat(input, walls, node):
    return [
        (1, n)
        for n in node.neighbors()
        if n.in_area(input) and (n in walls or n.get(input) != "#")
    ]


def distance_map(input, p):
    dist = {p: 0}
    wave = [p]
    for i in count(1):
        wave = [
            n
            for p in wave
            for n in p.neighbors()
            if n not in dist and n.get(input) != "#"
        ]
        if not wave:
            break
        for p in wave:
            dist[p] = i
    return dist


def find_path_in_distance_map(dist, start, finish):
    p = start
    path = [p]
    while p != finish:
        p = next(n for n in p.neighbors() if dist.get(n) == dist[p] - 1)
        path.append(p)
    return path


def try_cheats(input, dist, p, n):
    for i in n.neighbors():
        if i in dist and p != i and dist[p] - dist[i] > 2:
            yield (p, i), dist[p] - dist[i] - 2


def find_cheats(input, ps):
    start = find_tile(input, "S")
    finish = find_tile(input, "E")
    dist = distance_map(input, finish)
    path = find_path_in_distance_map(dist, start, finish)

    cheats = {}
    for p in path:
        for n in p.neighbors():
            if n.get(input) == "#":
                cheats.update(try_cheats(input, dist, p, n))

    return cheats.values()


def part1(input):
    return sum(int(d >= 100) for d in find_cheats(input, 2))


def part2(input):
    return sum(int(d >= 100) for d in find_cheats(input, 20))


def main():
    with open("../input/day_20.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def test_part1():
    cheats = find_cheats(parse_input(EXAMPLE_1), 2)
    assert Counter(cheats) == {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }


def test_part2():
    cheats = find_cheats(parse_input(EXAMPLE_1), 20)
    assert Counter(c for c in cheats if c > 50) == {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }
