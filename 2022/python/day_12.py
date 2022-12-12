from functools import partial

from astar import astar


def parse_input(input):
    return dict(
        ((x, y), ch)
        for (y, line) in enumerate(input.strip().splitlines())
        for (x, ch) in enumerate(line.strip())
    )


def neighbours(point):
    x, y = point
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def find_vertices(input):
    return ((v, p) for (p, v) in input.items() if v in ("S", "E"))


def elevation(ch):
    if ch == "S":
        return 0
    elif ch == "E":
        return 26
    else:
        return ord(ch) - ord("a")


def adjacent(input, v):
    for n in neighbours(v):
        if n not in input:
            continue
        if elevation(input[n]) <= elevation(input[v]) + 1:
            yield 1, n


def shortest_path(input, start):
    is_target = lambda v: input[v] == "E"
    h = lambda _: 1
    path = astar(start, partial(adjacent, input), h, is_target)
    return len(path) - 1 if path is not None else float("inf")


def part1(input):
    start = next(p for (p, v) in input.items() if v == "S")
    return shortest_path(input, start)


def part2(input):
    return min(shortest_path(input, p) for (p, v) in input.items() if v in ["a", "S"])


def main():
    with open("../input/day_12.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 31


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 29
