from lib import Vector


def parse_input(input):
    return input.strip().splitlines()


def is_valid(m, v):
    return 0 <= v.x < len(m[0]) and 0 <= v.y < len(m)


def find_start(m):
    return next(Vector(y, line.index("S")) for y, line in enumerate(m) if "S" in line)


def part1(input, steps=64):
    start = find_start(input)
    wave = {start}
    for _ in range(steps):
        wave = set(
            n
            for v in wave
            for n in v.neighbors()
            if is_valid(input, n) and input[n.y][n.x] == "."
        )
    return len(wave) + 1


def part2(input):
    pass


def main():
    with open("../input/day_21.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1), steps=6) == 16
