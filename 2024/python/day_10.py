from lib import Vector


def parse_input(input):
    return [[int(ch) for ch in line.strip()] for line in input.strip().splitlines()]


def find_start(input):
    return (
        Vector(x, y)
        for y, line in enumerate(input)
        for x, i in enumerate(line)
        if i == 0
    )


def count_trails(input, start):
    visited = set()
    wave = {start}
    for i in range(1, 10):
        if not wave:
            return 0
        visited.update(wave)
        wave = set(
            n
            for v in wave
            for n in v.neighbors()
            if n not in visited and n.get(input) == i
        )

    return len(wave)


def part1(input):
    return sum(count_trails(input, start) for start in find_start(input))


def count_distinct_trails(input, v, i):
    if i == 9:
        return 1

    return sum(
        count_distinct_trails(input, n, i + 1)
        for n in v.neighbors()
        if n.get(input) == i + 1
    )


def part2(input):
    return sum(count_distinct_trails(input, start, 0) for start in find_start(input))


def main():
    with open("../input/day_10.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 36


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 81
