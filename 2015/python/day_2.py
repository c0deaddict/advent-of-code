def parse_input(input):
    return [list(map(int, line.split("x"))) for line in input.strip().splitlines()]


def wrapping_size(present):
    l, w, h = present
    sides = [l * w, w * h, h * l]
    return sum(2 * s for s in sides) + min(sides)


def part1(input):
    return sum(map(wrapping_size, input))


def part2(input):
    pass


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
2x3x4
"""

EXAMPLE_2 = """
1x1x10
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 58
    assert part1(parse_input(EXAMPLE_2)) == 43
