def parse_input(input):
    return {
        (x, y)
        for y, line in enumerate(input.strip().splitlines())
        for x, c in enumerate(line)
        if c == "@"
    }


def neighbors(x, y):
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]


def part1(input):
    return sum(1 for p in input if sum(1 for n in neighbors(*p) if n in input) < 4)


def part2(input):
    rolls = set(input)
    removed = 0
    while True:
        count = 0
        for p in set(rolls):
            if sum(1 for n in neighbors(*p) if n in rolls) < 4:
                count += 1
                rolls.remove(p)
        removed += count
        if count == 0:
            return removed


def main():
    with open("../input/day_4.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 13


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 43
