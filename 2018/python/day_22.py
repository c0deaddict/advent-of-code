import pytest
from collections import namedtuple
from enum import Enum
from functools import partial, reduce

from astar import astar

Position = namedtuple("Position", ["x", "y"])


class Tool(Enum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_GEAR = 2


class RegionType(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

    def tools(self):
        if self is self.ROCKY:
            return [Tool.TORCH, Tool.CLIMBING_GEAR]
        elif self is self.WET:
            return [Tool.NEITHER, Tool.CLIMBING_GEAR]
        elif self is self.NARROW:
            return [Tool.NEITHER, Tool.TORCH]

    def can_use(self, tool):
        return tool in self.tools()


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.cache = {target: 0}

    def geologic_index(self, pos):
        if pos.y == 0:
            return pos.x * 16807
        elif pos.x == 0:
            return pos.y * 48271
        elif pos in self.cache:
            return self.cache[pos]
        else:
            a = self.erosion_level(Position(pos.x - 1, pos.y))
            b = self.erosion_level(Position(pos.x, pos.y - 1))
            result = a * b
            self.cache[pos] = result
            return result

    def erosion_level(self, pos):
        return (self.geologic_index(pos) + self.depth) % 20183

    def region_type(self, pos):
        return RegionType(self.erosion_level(pos) % 3)


def part1(cave):
    return sum(
        cave.region_type(Position(x, y)).value
        for x in range(0, cave.target.x + 1)
        for y in range(0, cave.target.y + 1)
    )

def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def adjacent_positions(pos):
    yield Position(pos.x + 1, pos.y)
    yield Position(pos.x, pos.y + 1)
    if pos.x > 0:
        yield Position(pos.x - 1, pos.y)
    if pos.y > 0:
        yield Position(pos.x, pos.y - 1)


def adjacent(cave, node):
    pos, tool = node

    for other_tool in cave.region_type(pos).tools():
        if tool != other_tool:
            yield 7, (pos, other_tool)

    for next_pos in adjacent_positions(pos):
        if cave.region_type(next_pos).can_use(tool):
            yield 1, (next_pos, tool)

def path_cost(path):
    time = 0
    for i in range(len(path)-1):
        if path[i+1][1] != path[i][1]:
            time += 7
        else:
            time += 1
    return time


def part2(cave):
    start = (Position(0, 0), Tool.TORCH)
    target = (cave.target, Tool.TORCH)
    h = lambda node: manhattan(node[0], cave.target)
    path = astar(start, partial(adjacent, cave), h, target)
    return path_cost(path)

def main():
    input = Cave(3198, Position(12, 757))
    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1(Cave(510, Position(10, 10))) == 114


def test_part2():
    assert part2(Cave(510, Position(10, 10))) == 45
