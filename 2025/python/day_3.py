import operator


def parse_input(input):
    return [[int(d) for d in bank] for bank in input.strip().splitlines()]


def max_joltage(bank, n):
    res = 0
    i = 0
    free = len(bank) - n
    for _ in range(n):
        # Find the maximum value and index in the range of choices.
        (k, v) = max(enumerate(bank[i : i + 1 + free]), key=operator.itemgetter(1))
        res = res * 10 + v
        i += k + 1
        free -= k
    return res


def part1(input):
    return sum(max_joltage(bank, 2) for bank in input)


def part2(input):
    return sum(max_joltage(bank, 12) for bank in input)


def main():
    with open("../input/day_3.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
987654321111111
811111111111119
234234234234278
818181911112111
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 357


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 3121910778619
