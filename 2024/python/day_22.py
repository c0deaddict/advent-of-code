def parse_input(input):
    return input.strip().splitlines()


def part1(input):
    pass


def part2(input):
    pass


def main():
    with open("../input/day_22.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 0
