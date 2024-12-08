from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations, count

from lib import Vector


@dataclass
class Map:
    width: int
    height: int
    antennas: dict[str, list[Vector]]


def parse_input(input) -> Map:
    contents = input.strip().splitlines()
    width = len(contents[0])
    height = len(contents)
    antennas = defaultdict(list)
    for y, line in enumerate(contents):
        for x, ch in enumerate(line):
            if ch != ".":
                antennas[ch].append(Vector(x, y))
    return Map(width, height, antennas)


def in_area(m: Map, p: Vector) -> bool:
    return 0 <= p.x < m.width and 0 <= p.y < m.height


def antenna_line(m: Map, i: Vector, j: Vector) -> set[Vector]:
    antinodes = set()
    d = i - j
    for k in count(0):
        p1 = i + d.scale(k)
        p2 = i - d.scale(k)
        if ia1 := in_area(m, p1):
            antinodes.add(p1)
        if ia2 := in_area(m, p2):
            antinodes.add(p2)
        if not (ia1 or ia2):
            break
    return antinodes


def part1(input):
    antinodes = set()
    for _, pos in input.antennas.items():
        for i, j in combinations(pos, 2):
            for p in antenna_line(input, i, j):
                di = p.manhattan(i)
                dj = p.manhattan(j)
                if di == dj * 2 or dj == di * 2:
                    antinodes.add(p)

    return len(antinodes)


def part2(input):
    antinodes = set()
    for _, pos in input.antennas.items():
        for i, j in combinations(pos, 2):
            antinodes.update(antenna_line(input, i, j))

    return len(antinodes)


def main():
    with open("../input/day_8.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 14


EXAMPLE_2 = """
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_2)) == 9
    assert part2(parse_input(EXAMPLE_1)) == 34
