def parse_input(input):
    return [
        [[int(i) for i in elf.split("-")] for elf in line.split(",")]
        for line in input.strip().splitlines()
    ]


def fully_contains(a, b):
    return b[0] >= a[0] and b[1] <= a[1]


def part1(input):
    return sum(
        1
        for pair in input
        if fully_contains(pair[0], pair[1]) or fully_contains(pair[1], pair[0])
    )


def overlap(a, b):
    return (
        fully_contains(a, b)
        or fully_contains(b, a)
        or (a[0] <= b[0] and a[1] >= b[0])
        or (a[0] <= b[1] and a[1] >= b[1])
    )


def part2(input):
    return sum(1 for pair in input if overlap(*pair))


def main():
    with open("../input/day_4.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 2


def test_part1():
    assert part2(parse_input(EXAMPLE_1)) == 4
