def parse_input(input):
    return [list(row) for row in input.strip().splitlines()]


def expansion(input):
    xs = set(
        x for x, _ in enumerate(input[0]) if not any(row[x] == "#" for row in input)
    )
    ys = set(y for y, row in enumerate(input) if "#" not in row)
    return xs, ys


def expand(exp, p, n):
    xs, ys = exp
    return (
        p[0] + sum(n-1 for x in xs if x < p[0]),
        p[1] + sum(n-1 for y in ys if y < p[1]),
    )


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shortest_paths(input, n):
    exp = expansion(input)
    galaxies = set(
        expand(exp, (x, y), n)
        for y, row in enumerate(input)
        for x, cell in enumerate(row)
        if cell == "#"
    )
    return sum(manhattan(a, b) for a in galaxies for b in galaxies if a != b) // 2


def part1(input):
    return shortest_paths(input, 2)


def part2(input):
    return shortest_paths(input, 1_000_000)


def main():
    with open("../input/day_11.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 374


def test_part2_10():
    assert shortest_paths(parse_input(EXAMPLE_1), 10) == 1030

def test_part2_100():
    assert shortest_paths(parse_input(EXAMPLE_1), 100) == 8410
