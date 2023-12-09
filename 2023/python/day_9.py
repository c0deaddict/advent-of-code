import re
from functools import partial


def parse_input(input):
    return [
        [int(d) for d in re.findall(r"-?\d+", line)]
        for line in input.strip().splitlines()
    ]


def predict(forward: bool, series: list[int]):
    if set(series) == {0}:
        return 0
    else:
        d = predict(forward, [j - i for i, j in zip(series, series[1:])])
        return series[-1] + d if forward else series[0] - d


def part1(input):
    return sum(map(partial(predict, True), input))


def part2(input):
    return sum(map(partial(predict, False), input))


def main():
    with open("../input/day_9.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 114


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 2
