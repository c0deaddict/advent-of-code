from functools import partial
from itertools import chain

from astar import astar


def parse_input(input):
    return int(input.strip())


def is_wall(input, pos):
    x, y = pos
    n = x * x + 3 * x + 2 * x * y + y + y * y + input
    bits = f"{n:b}"
    ones = sum(1 for b in bits if b == "1")
    return ones % 2 == 1


def is_valid(pos):
    x, y = pos
    return x >= 0 and y >= 0


def neighbors(pos):
    x, y = pos
    return filter(is_valid, [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)])


def adjacent(input, pos):
    for n in neighbors(pos):
        if not is_wall(input, n):
            yield (1, n)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shortest_path(input, target):
    start = (1, 1)
    h = partial(manhattan, target)
    is_target = lambda n: n == target
    adj = partial(adjacent, input)
    return len(astar(start, adj, h, is_target)) - 1


def part1(input):
    return shortest_path(input, (31, 39))


def part2(input):
    start = (1, 1)
    frontier = set([start])
    visited = set([start])
    for dist in range(50):
        frontier = set(
            n
            for n in chain(*(neighbors(p) for p in frontier))
            if not is_wall(input, n) and n not in visited
        )
        if len(frontier) == 0:
            break

        visited.update(frontier)

    return len(visited)


def main():
    with open("../input/day_13.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert shortest_path(10, (7, 4)) == 11
