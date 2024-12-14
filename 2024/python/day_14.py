import re
from dataclasses import dataclass
from functools import reduce
from itertools import count
import operator

from lib import Vector


@dataclass
class Robot:
    p: Vector
    v: Vector


def parse_robot(line):
    s = list(map(int, re.findall(r"-?\d+", line)))
    return Robot(Vector(*s[:2]), Vector(*s[2:]))


def parse_input(input):
    return list(map(parse_robot, input.strip().splitlines()))


def safety_factor(size, robots):
    middle = size // Vector(2, 2)
    qsum = [0] * 4
    for p in robots:
        if p.x == middle.x or p.y == middle.y:
            continue
        qx = p.x > middle.x
        qy = p.y > middle.y
        qi = int(qx) + int(qy) * 2
        qsum[qi] += 1
    return reduce(operator.mul, qsum)


def part1(input, w=101, h=103, t=100):
    size = Vector(w, h)
    robots = [(r.p + r.v.scale(t)).modulo(size) for r in input]
    return safety_factor(size, robots)


def print_robots(size, robots):
    robots = set(robots)
    for y in range(size.y):
        line = ""
        for x in range(size.x):
            if Vector(x, y) in robots:
                line += "X"
            else:
                line += " "
        print(line)
    print()


def neighbor_ratio(robots):
    robots = set(robots)
    count = sum(int(any(n in robots for n in p.all_neighbors())) for p in robots)
    return count / float(len(robots))


def part2(input):
    size = Vector(101, 103)
    robots = [r.p for r in input]
    for t in count(1):
        robots = [(p + input[i].v).modulo(size) for i, p in enumerate(robots)]
        if neighbor_ratio(robots) > 0.5:
            print(t)
            print_robots(size, robots)


def main():
    with open("../input/day_14.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1), w=11, h=7) == 12
