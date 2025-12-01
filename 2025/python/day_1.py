def parse_input(input):
    return [(line[0], int(line[1:])) for line in input.strip().splitlines()]


def part1(input):
    dial = 50
    zeroes = 0
    for dir, clicks in input:
        if dir == "L":
            clicks = -clicks
        dial = (dial + clicks) % 100
        if dial == 0:
            zeroes += 1
    return zeroes


def part2(input):
    dial = 50
    zeroes = 0
    for dir, clicks in input:
        d = -1 if dir == "L" else +1
        for _ in range(clicks):
            dial = (dial + d) % 100
            if dial == 0:
                zeroes += 1
    return zeroes


def main():
    with open("../input/day_1.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 3


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 6
