import math
import re
from dataclasses import dataclass
from functools import reduce
from typing import Callable


@dataclass
class Map:
    instr: str
    edges: dict[str, tuple[str, str]]


def parse_input(input):
    instr, edges = input.strip().split("\n\n")
    edges = {
        m.group(1): (m.group(2), m.group(3))
        for m in re.finditer(r"(\w{3}) = \((\w{3}), (\w{3})\)", edges)
    }
    return Map(instr=instr, edges=edges)


def path(m: Map, start: str, goal: Callable[[str], bool]) -> int:
    cur = start
    count = 0
    while not goal(cur):
        d = m.instr[count % len(m.instr)]
        cur = m.edges[cur][0 if d == "L" else 1]
        count += 1
    return count


def part1(input):
    return path(input, "AAA", lambda v: v == "ZZZ")


def part2(input):
    paths = [
        path(input, v, lambda v: v.endswith("Z"))
        for v in input.edges.keys()
        if v.endswith("A")
    ]
    return reduce(math.lcm, paths)


def main():
    with open("../input/day_8.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def test_part1_example1():
    assert part1(parse_input(EXAMPLE_1)) == 2


def test_part1_example2():
    assert part1(parse_input(EXAMPLE_2)) == 6


EXAMPLE_3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_3)) == 6
