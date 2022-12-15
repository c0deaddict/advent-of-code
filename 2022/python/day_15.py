import re
from dataclasses import dataclass
from operator import itemgetter


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


def parse_line(line):
    sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
    return Point(sx, sy), Point(bx, by)


def parse_input(input):
    return [parse_line(line) for line in input.strip().splitlines()]


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def add_range(ranges, start, end):
    for other_start, other_end in ranges:
        # range is fully contained in other
        if start >= other_start and end <= other_end:
            return
        # range partially overlaps with other
        if (start < other_start and end >= other_start) or (
            start <= other_end and end > other_end
        ):
            ranges.remove((other_start, other_end))
            return add_range(ranges, min(start, other_start), max(end, other_end))
        # other is fully contained in range
        if other_start >= start and other_end <= end:
            ranges.remove((other_start, other_end))

    ranges.append((start, end))


def part1(input, y=2000000):
    ranges = []
    beacons = set()
    for sensor, beacon in input:
        dist = manhattan(sensor, beacon)
        dy = abs(sensor.y - y)
        dx = dist - dy
        if dx >= 0:
            add_range(ranges, sensor.x - dx, sensor.x + dx)

        if beacon.y == y:
            beacons.add(beacon)

    return sum(end - start + 1 for start, end in ranges) - len(beacons)


def part2(input, search=4000000):
    for y in range(0, search + 1):
        ranges = []
        for sensor, beacon in input:
            dist = manhattan(sensor, beacon)
            dy = abs(sensor.y - y)
            dx = dist - dy
            if dx >= 0:
                add_range(ranges, sensor.x - dx, sensor.x + dx)

        x = ranges[0][0]
        for start, end in sorted(ranges, key=itemgetter(0)):
            if x > search:
                break
            if x >= 0 and x < start:
                return x * 4000000 + y
            else:
                x = end + 1


def main():
    with open("../input/day_15.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1), y=10) == 26


def test_part2():
    assert part2(parse_input(EXAMPLE_1), search=20) == 56000011
