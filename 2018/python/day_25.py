import pytest
from itertools import combinations
from typing import List
import operator
import copy


def manhattan(a, b) -> int:
    return sum(abs(pa - pb) for (pa, pb) in zip(a, b))


def parse_input(input):
    return [tuple(map(int, line.split(","))) for line in input.strip().splitlines()]


def part1(input):
    constellations = []
    for p in input:
        matched = None
        for c in constellations:
            if any(manhattan(p, v) <= 3 for v in c):
                if matched is None:
                    c.add(p)
                    matched = c
                else:
                    matched.update(c)
                    c.clear()

        if matched is None:
            constellations.append(set([p]))

        constellations = [c for c in constellations if len(c)]

    return len(constellations)


def main():
    with open("../input/day_25.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
"""

EXAMPLE_DATA_2 = """
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
"""

EXAMPLE_DATA_3 = """
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2
"""

EXAMPLE_DATA_4 = """
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
"""


def test_part1_example1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 2


def test_part1_example2():
    assert part1(parse_input(EXAMPLE_DATA_2)) == 4


def test_part1_example3():
    assert part1(parse_input(EXAMPLE_DATA_3)) == 3


def test_part1_example4():
    assert part1(parse_input(EXAMPLE_DATA_4)) == 8
