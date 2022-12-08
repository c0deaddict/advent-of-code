from itertools import chain


def parse_input(input):
    return [list(map(int, list(line))) for line in input.strip().splitlines()]


def find_visible(input, line):
    top = -1
    for (x, y) in line:
        tree = input[y][x]
        if tree > top:
            yield (x, y)
            top = tree


def part1(input):
    height = len(input)
    width = len(input[0])
    visible = set()
    for y in range(height):
        visible.update(find_visible(input, ((x, y) for x in range(width))))
        visible.update(find_visible(input, ((width - 1 - x, y) for x in range(width))))
    for x in range(width):
        visible.update(find_visible(input, ((x, y) for y in range(height))))
        visible.update(
            find_visible(input, ((x, height - 1 - y) for y in range(height)))
        )
    return len(visible)


def viewing_distance(input, start, line):
    count = 0
    for (x, y) in line:
        count += 1
        if input[y][x] >= start:
            break
    return count


def scenic_score(input, x, y):
    height = len(input)
    width = len(input[0])
    tree = input[y][x]
    x1 = viewing_distance(input, tree, ((i, y) for i in range(x - 1, -1, -1)))
    x2 = viewing_distance(input, tree, ((i, y) for i in range(x + 1, width)))
    y1 = viewing_distance(input, tree, ((x, i) for i in range(y - 1, -1, -1)))
    y2 = viewing_distance(input, tree, ((x, i) for i in range(y + 1, height)))
    return x1 * x2 * y1 * y2


def part2(input):
    return max(
        scenic_score(input, x, y)
        for y, line in enumerate(input)
        for x, _ in enumerate(line)
    )


def main():
    with open("../input/day_8.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
30373
25512
65332
33549
35390
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 21


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 8
