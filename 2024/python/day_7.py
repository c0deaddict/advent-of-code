import re
import operator
from itertools import product


def parse_input(input):
    return [
        [int(i) for i in re.findall(r"\d+", line)]
        for line in input.strip().splitlines()
    ]


def compute(values, ops):
    result = values[0]
    for i, op in zip(values[1:], ops):
        result = op(result, i)
    return result


def is_solveable(operators, test, *values):
    for ops in product(operators, repeat=len(values) - 1):
        if compute(values, ops) == test:
            return True
    return False


def part1(input):
    operators = [operator.add, operator.mul]
    return sum(eq[0] for eq in input if is_solveable(operators, *eq))


def concat(left, right):
    return int(str(left) + str(right))


def part2(input):
    operators = [operator.add, operator.mul, concat]
    return sum(eq[0] for eq in input if is_solveable(operators, *eq))


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def test_compute():
    assert compute([1, 2, 3], [operator.mul, operator.add]) == 5


def test_concat():
    assert concat(12, 345) == 12345


def test_compute_with_concat():
    assert compute([6, 8, 6, 15], [operator.mul, concat, operator.mul]) == 7290


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 3749


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 11387
