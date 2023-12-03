import re
from dataclasses import dataclass


@dataclass(frozen=False)
class Input:
    numbers: list
    symbols: dict


def parse_input(input):
    i = Input(numbers=[], symbols={})
    for y, row in enumerate(input.strip().splitlines()):
        for m in re.finditer(r"\d+", row):
            i.numbers.append((int(m.group()), set((x, y) for x in range(*m.span()))))

        for x, c in enumerate(row):
            if c == ".":
                continue
            elif not c.isdigit():
                i.symbols[(x, y)] = c
    return i


def neigh(x, y):
    return set(
        [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]
    )


def part1(input):
    return sum(
        n
        for n, ps in input.numbers
        if any(pn in input.symbols for p in ps for pn in neigh(*p))
    )


def gear_ratios(input):
    for p, s in input.symbols.items():
        if s != "*":
            continue
        nadj = [n for n, ps in input.numbers if ps.intersection(neigh(*p))]
        if len(nadj) == 2:
            yield nadj[0] * nadj[1]


def part2(input):
    return sum(gear_ratios(input))


def main():
    with open("../input/day_3.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 4361


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 467835
