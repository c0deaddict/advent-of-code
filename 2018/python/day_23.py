import pytest
import re
from collections import namedtuple
from operator import attrgetter
from functools import reduce
from pprint import pprint
from itertools import combinations

Nanobot = namedtuple("Nanobot", ["x", "y", "z", "r"])


def parse_nanobot(line):
    m = re.match(r"^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$", line)
    return Nanobot(*map(int, m.groups()))


def parse_input(input):
    return [parse_nanobot(line) for line in input.strip().splitlines()]


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def part1(input):
    strongest = max(input, key=attrgetter("r"))
    return len([bot for bot in input if manhattan(bot, strongest) <= strongest.r])


def overlap(a, b):
    return manhattan(a, b) <= a.r + b.r


def intersect(a, b):
    # manhattan(a, p) == a.r
    # manhattan(b, p) == b.r

    # abs(a.x - p.x) + abs(a.y - p.y) + abs(a.z - p.z) == a.r
    # abs(b.x - p.x) + abs(b.y - p.y) + abs(b.z - p.z) == b.r

    # abs(a.x - p.x) + abs(a.y - p.y) + abs(a.z - p.z) - a.r == 0
    # abs(b.x - p.x) + abs(b.y - p.y) + abs(b.z - p.z) - b.r == 0

    r = a.r + b.r
    dx, dy, dz = (b.x - a.x) / r, (b.y - a.y) / r, (b.z - a.z) / r
    print(a.x + dx * a.r, a.y + dy * a.r, a.z + dz * a.r)


def part2(input):
    # todo: need to find a cluster in which *all* bots overlap, not just `a` with all other, but also all of:
    # foreach pair (a,b) in cluster: a and b overlap.
    # idea: first sort out what the largest clusters are, there are probably more.
    # then for each cluster find the pair that has exactly one point of overlap.
    # this pair must be the intersection point of the whole cluster.
    for bot in input:
        cluster = [other for other in input if overlap(bot, other)]
        if len(cluster) < 2:
            continue
        if not all(overlap(a, b) for (a, b) in combinations(cluster, 2)):
            continue
        try:
            # TODO: determine intersection of a,b (this can be a line?)
            print(
                next(
                    intersect(a, b)
                    for (a, b) in combinations(cluster, 2)
                    if manhattan(a, b) == a.r + b.r
                )
            )
        except StopIteration:
            pass


def main():
    with open("../input/day_23.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 7


EXAMPLE_DATA_2 = """
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_2)) == 36
