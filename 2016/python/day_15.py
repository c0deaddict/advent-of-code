import re
from dataclasses import dataclass
from itertools import count


@dataclass
class Entry:
    disc: int
    size: int
    time: int
    position: int


def parse_input(input):
    return [
        Entry(*map(int, re.findall(r"\d+", line)))
        for line in input.strip().splitlines()
    ]


def solve(input):
    for t in count(start=0):
        if all((t + e.disc + e.position) % e.size == 0 for e in input):
            return t


def part1(input):
    return solve(input)


def part2(input):
    return solve(input + [Entry(len(input) + 1, 11, 0, 0)])


def main():
    with open("../input/day_15.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 5


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) is None
