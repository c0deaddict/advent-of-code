import re
import math
from functools import reduce
import operator


def parse_input(input):
    return [
        [int(s) for s in re.findall(r"\d+", line)]
        for line in input.strip().splitlines()
    ]


def product(it):
    return reduce(operator.mul, it)


def count_wins(time, distance):
    d = math.sqrt(time * time - 4 * (distance + 1))
    x1 = (-time + d) / -2
    x2 = (-time - d) / -2
    return 1 + math.floor(x2) - math.ceil(x1)


def part1(input):
    return product(count_wins(time, distance) for time, distance in zip(*input))


def part2(input):
    time, distance = [int("".join(map(str, line))) for line in input]
    return count_wins(time, distance)


def main():
    with open("../input/day_6.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Time:      7  15   30
Distance:  9  40  200
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 288


# def test_part2():
#     assert part2(parse_input(EXAMPLE_1)) == 71503
