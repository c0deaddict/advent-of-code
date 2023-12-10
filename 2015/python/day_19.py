from functools import partial
from dataclasses import dataclass

from astar import astar


@dataclass
class Medicine:
    replacements: list[tuple[str, str]]
    molecule: str


def parse_replacements(replacements) -> list[tuple[str, str]]:
    return [line.strip().split(" => ", 2) for line in replacements.strip().splitlines()]


def parse_input(input):
    blocks = input.strip().split("\n\n")
    return Medicine(parse_replacements(blocks[0]), blocks[1].strip())


def do_replacements(replacements, molecule):
    results = set()
    for i in range(len(molecule)):
        for from_, to in replacements:
            if molecule[i : i + len(from_)] == from_:
                results.add(molecule[:i] + to + molecule[i + len(from_) :])
    return results


def part1(input):
    return len(do_replacements(input.replacements, input.molecule))


def adjacent(replacements, node):
    return ((1, next) for next in do_replacements(replacements, node))


def part2(input):
    reverse_replacements = [(to, from_) for from_, to in input.replacements]
    start = input.molecule
    h = len
    is_target = lambda m: m == "e"
    adj = partial(adjacent, reverse_replacements)
    return len(astar(start, adj, h, is_target)) - 1


def main():
    with open("../input/day_19.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
H => HO
H => OH
O => HH
"""


def test_part1():
    replacements = parse_replacements(EXAMPLE_DATA_1)
    assert part1(Medicine(replacements, "HOH")) == 4
    assert part1(Medicine(replacements, "HOHOHO")) == 7


EXAMPLE_DATA_2 = """
e => H
e => O
H => HO
H => OH
O => HH
"""


def test_part2():
    replacements = parse_replacements(EXAMPLE_DATA_2)
    assert part2(Medicine(replacements, "HOH")) == 3
    assert part2(Medicine(replacements, "HOHOHO")) == 6
