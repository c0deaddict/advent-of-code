import re
from dataclasses import dataclass
from collections import defaultdict
from operator import itemgetter
from copy import deepcopy


@dataclass
class Move:
    count: int
    src: int
    dst: int


def parse_crates(input):
    crates = defaultdict(list)
    for line in input.splitlines():
        for m in re.finditer(r"[A-Z]", line):
            stack = 1 + (m.start() - 1) // 4
            crates[stack].insert(0, m.group())
    return crates


def parse_moves(input):
    return [Move(*map(int, re.findall(r"\d+", line))) for line in input.splitlines()]


def parse_input(input):
    crates, moves = input.split("\n\n")
    return parse_crates(crates), parse_moves(moves)


def top_crates(crates):
    return "".join(stack[-1] for _, stack in sorted(crates.items(), key=itemgetter(0)))


def part1(input):
    crates, moves = input
    crates = deepcopy(crates)
    for m in moves:
        for _ in range(m.count):
            crates[m.dst].append(crates[m.src].pop())
    return top_crates(crates)


def part2(input):
    crates, moves = input
    crates = deepcopy(crates)
    for m in moves:
        for crate in reversed([crates[m.src].pop() for i in range(m.count)]):
            crates[m.dst].append(crate)
    return top_crates(crates)


def main():
    with open("../input/day_5.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == "CMZ"


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == "MCD"
