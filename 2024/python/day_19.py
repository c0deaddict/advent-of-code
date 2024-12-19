from functools import cache


def parse_input(input):
    towels, patterns = input.strip().split("\n\n")
    return towels.split(", "), patterns.splitlines()


def check_pattern(towels, pattern):
    if not pattern:
        return True

    for t in towels:
        if pattern[: len(t)] == t:
            if check_pattern(towels, pattern[len(t) :]):
                return True
    return False


def part1(input):
    towels, patterns = input
    return sum(int(check_pattern(towels, p)) for p in patterns)


@cache
def count_options(towels, pattern):
    if not pattern:
        return 1

    count = 0
    for t in towels:
        if pattern[: len(t)] == t:
            count += count_options(towels, pattern[len(t) :])
    return count


def part2(input):
    towels, patterns = input
    return sum(count_options(tuple(towels), p) for p in patterns)


def main():
    with open("../input/day_19.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgbw
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 6


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 16
