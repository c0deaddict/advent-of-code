def parse_input(input):
    return [tuple(map(int, line.split(",", 2))) for line in input.strip().splitlines()]


def area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def part1(input):
    return max(
        map(
            lambda pair: area(*pair),
            [(a, b) for i, a in enumerate(input) for b in input[i + 1 :]],
        )
    )


def minmax(a, b):
    return (min(a[0], b[0]), min(a[1], b[1])), (max(a[0], b[0]), max(a[1], b[1]))


def intersects(rectangle, line):
    (r1x, r1y), (r2x, r2y) = rectangle
    (l1x, l1y), (l2x, l2y) = line
    if l1y == l2y:
        # horizontal
        return l1y > r1y and l1y < r2y and l1x < r2x and l2x > r1x
    else:
        # vertical
        return l1x > r1x and l1x < r2x and l1y < r2y and l2y > r1y


def is_filled(input, rectangle):
    return not any(
        intersects(rectangle, minmax(*line))
        for line in zip(input, input[1:] + [input[0]])
    )


def part2(input):
    return max(
        map(
            lambda pair: area(*pair),
            [
                (a, b)
                for i, a in enumerate(input)
                for b in input[i + 1 :]
                if is_filled(input, minmax(a, b))
            ],
        )
    )


def main():
    with open("../input/day_9.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 50


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 24
