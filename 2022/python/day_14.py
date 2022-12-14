from functools import reduce
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


def parse_rock(line):
    return [Point(*map(int, p.split(","))) for p in line.split(" -> ")]


def parse_input(input):
    return [parse_rock(line) for line in input.strip().splitlines()]


def sign(v):
    return 0 if v == 0 else (1 if v > 0 else -1)


def trace_rock(rock):
    for a, b in zip(rock, rock[1:]):
        dx = sign(b.x - a.x)
        dy = sign(b.y - a.y)
        if dx != 0:
            yield from (Point(x, a.y) for x in range(a.x, b.x + dx, dx))
        else:
            yield from (Point(a.x, y) for y in range(a.y, b.y + dy, dy))


def dimensions(points):
    minx = min(points, key=lambda p: p.x).x
    maxx = max(points, key=lambda p: p.x).x
    miny = min(points, key=lambda p: p.y).y
    maxy = max(points, key=lambda p: p.y).y
    return (minx, maxx), (miny, maxy)


def draw(rock, sand):
    points = rock.union(sand)
    (minx, maxx), (miny, maxy) = dimensions(points)

    print()
    for y in range(miny - 1, maxy + 2):
        print(
            "".join(
                "#" if Point(x, y) in rock else ("o" if Point(x, y) in sand else ".")
                for x in range(minx - 1, maxx + 2)
            )
        )


def fill_sand(rock, stop):
    sand = set()
    while True:
        grain = Point(500, 0)
        while True:
            moves = [
                Point(grain.x, grain.y + 1),
                Point(grain.x - 1, grain.y + 1),
                Point(grain.x + 1, grain.y + 1),
            ]
            n = next((p for p in moves if p not in rock and p not in sand), None)
            if n is None:
                if grain in sand:
                    return sand
                sand.add(grain)
                break
            if stop(n):
                return sand
            grain = n


def part1(input):
    rock = reduce(set.union, map(trace_rock, input), set())
    abyss = 1 + max(p.y for p in rock)
    sand = fill_sand(rock, lambda n: n.y >= abyss)
    draw(rock, sand)
    return len(sand)


def part2(input):
    rock = reduce(set.union, map(trace_rock, input), set())
    floor = 2 + max(p.y for p in rock)
    rock.update(trace_rock([Point(500 - floor, floor), Point(500 + floor, floor)]))
    sand = fill_sand(rock, lambda _: False)
    draw(rock, sand)
    return len(sand)


def main():
    with open("../input/day_14.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 24


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 93
