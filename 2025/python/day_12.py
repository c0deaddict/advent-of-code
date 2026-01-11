import re


def parse_region(line):
    x, y, *shapes = map(int, re.findall(r"\d+", line))
    return (x, y), shapes


def parse_input(input):
    parts = input.strip().split("\n\n")
    regions = [parse_region(line) for line in parts.pop().splitlines()]
    shapes = [tuple(part.strip().splitlines()[1:]) for part in parts]
    return shapes, regions


def rotate_right(shape):
    height = len(shape)
    width = len(shape[0])
    return tuple(
        tuple(shape[y][x] for y in range(height - 1, -1, -1)) for x in range(width)
    )


def rotations(shape):
    yield shape
    for _ in range(3):
        shape = rotate_right(shape)
        yield shape


def flip_horizontal(shape):
    return tuple(tuple(reversed(line)) for line in shape)


def flip_vertical(shape):
    return tuple(reversed(shape))


def transforms(shape):
    return (
        set(rotations(shape))
        | set(rotations(flip_horizontal(shape)))
        | set(rotations(flip_vertical(shape)))
        | set(rotations(flip_horizontal(flip_vertical(shape))))
    )


def area(shape):
    return sum(line.count("#") for line in shape)


def fit_presents(shapes, width, height, counts):
    if (
        sum(count * area(shape) for count, shape in zip(counts, shapes))
        > width * height
    ):
        return False

    return True


def part1(input):
    shapes, regions = input
    return sum(
        fit_presents(shapes, width, height, counts)
        for (width, height), counts in regions
    )


def part2(input):
    pass


def main():
    with open("../input/day_12.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 2


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) is None
