import pytest
import re
from collections import namedtuple
from operator import attrgetter
from functools import cmp_to_key, partial
from pprint import pprint
from itertools import combinations

from dataclasses import dataclass
import itertools


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    z: int


@dataclass(eq=True, frozen=True)
class Nanobot(Point):
    r: int


def parse_nanobot(line):
    return Nanobot(*map(int, re.findall(r"-?\d+", line)))


def parse_input(input):
    return [parse_nanobot(line) for line in input.strip().splitlines()]


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def part1(input):
    strongest = max(input, key=attrgetter("r"))
    return len([bot for bot in input if manhattan(bot, strongest) <= strongest.r])


def overlap(a, b):
    return manhattan(a, b) <= a.r + b.r


def direction(a, b):
    def compare(i, j):
        if i < j:
            return -1
        elif i > j:
            return 1
        else:
            return 0

    return [
        compare(b.x, a.x),
        compare(b.y, a.y),
        compare(b.z, a.z),
    ]


# https://martin-thoma.com/solving-linear-equations-with-gaussian-elimination/
def gauss(A):
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n + 1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            c = -A[k][i] // A[i][i]
            for j in range(i, n + 1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (A[i][n] // A[i][i]) if A[i][i] != 0 else 0
        for k in range(i - 1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x


def part2(input):
    # Find the largest cluster by starting with the bot that overlaps with the
    # most other bots.
    overlapping = {a: [b for b in input if overlap(a, b)] for a in input}
    cluster = set(max(overlapping.values(), key=len))

    # Purge the cluster from bots that are not fully connected. Preferring the
    # bots that have a higher overlapping count.
    for (a, b) in combinations(cluster, 2):
        if a not in cluster or b not in cluster:
            continue
        if not overlap(a, b):
            cluster.remove(b if len(overlapping[a]) > len(overlapping[b]) else a)

    # Build up a list of equations for x,y,z points that are exactly on the
    # intersecting plane between pair of nanobots (a, b).
    eq = list()
    for (a, b) in combinations(cluster, 2):
        if manhattan(a, b) == a.r + b.r:
            dx, dy, dz = direction(a, b)
            # dx(p.x - a.x) +  dy(p.y - a.y) + dz(p.z - a.z) = a.r
            # ==>
            # dx*p.x - d.x*a.x + ... = a.r
            # ==>
            # dx*p.x + dy*p.y + dz*p.z = a.r + dx*a.x + dy*a.y + dz*a.z
            eq.append((dx, dy, dz, a.r + dx * a.x + dy * a.y + dz * a.z))

            # dx(b.x - p.x) +  dy(b.y - p.y) + dz(b.z - p.z) = b.r
            # ==>
            # dx*b.x - dx*p.x + ... = b.r
            # ==>
            # -dx*p.x + -dy*p.y + -dz*p.z = b.r - dx*b.x - dy*b.y - dz*b.z
            eq.append((-dx, -dy, -dz, b.r - dx * b.x - dy * b.y - dz * b.z))

    # Filter out duplicates and inverted equations.
    eq_set = set()
    for e in eq:
        if (-e[0], -e[1], -e[2], -e[3]) not in eq_set:
            eq_set.add(e)

    # Convert eq_set to a matrix that can be used by Gaussian Elimation. The
    # (non-augmented) matrix must be square, so we might need to add extra
    # always-zero variables.
    m = list()
    for e in eq_set:
        row = list(e[:-1]) + [0] * (len(eq_set) - len(e) + 1) + [e[-1]]
        m.append(row)

    [x, y, z, *rest] = gauss(m)
    return manhattan(Point(x, y, z), Point(0, 0, 0))


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
