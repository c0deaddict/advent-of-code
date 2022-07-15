import pytest
from collections import namedtuple
import operator
from functools import reduce

def parse_input(input):
    return dict(
        ((x, y), int(height))
        for (y, line) in enumerate(input.strip().splitlines())
        for (x, height) in enumerate(line.strip())
    )

def neighbours(point):
    x, y = point
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

def low_points(input):
    return (
        (p, h) for (p, h) in input.items()
        if all(input.get(n, 9) > h for n in neighbours(p))
    )

def part1(input):
    return sum(h + 1 for (_, h) in low_points(input))

def discover_basin(input, start):
    basin = set()
    queue = [start]
    while len(queue):
        point = queue.pop()
        if input.get(point, 9) == 9:
            continue # At edge

        basin.add(point)

        for n in neighbours(point):
            if n not in basin:
                queue.append(n)

    return basin

def part2(input):
    visited = set()

    def discover_basin_and_account(start):
        basin = discover_basin(input, start)
        visited.update(basin)
        return len(basin)

    basins = (
        discover_basin_and_account(start)
        for (start, _) in low_points(input)
        if start not in visited
    )

    return reduce(operator.mul, sorted(basins, reverse=True)[:3])

def main():
    with open('../input/day_09.txt', 'r') as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))

if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""

def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 15

def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_1)) == 1134
