import pytest
from collections import namedtuple
from enum import Enum
from queue import PriorityQueue
import functools

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


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


# https://bugs.python.org/issue31145
@functools.total_ordering
class Prio:
    def __init__(self, f, node):
        self.f = f
        self.node = node

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f


def reconstruct_path(came_from, current):
    time = 0
    path = [current]
    _, prev_tool = current
    while current in came_from:
        current = came_from[current]
        path.append(current)
        _, tool = current
        if tool != prev_tool:
            time += 7
            prev_tool = tool
        else:
            time += 1
    path.reverse()
    return time


def part2(cave):
    start = (Position(0, 0), Tool.TORCH)
    open_queue = PriorityQueue()
    open_queue.put(Prio(0, start))
    open_set = set([start])
    came_from = dict()
    g_score = {start: 0}

    while not open_queue.empty():
        current = open_queue.get()
        open_set.remove(current.node)

        if current.node == (cave.target, Tool.TORCH):
            return reconstruct_path(came_from, current.node)

        for time, child in adjacent(cave, current.node):
            g = g_score[current.node] + time
            if child not in g_score or g < g_score[child]:
                came_from[child] = current.node
                g_score[child] = g
                f = g + manhattan(child[0], cave.target)
                if child not in open_set:
                    open_set.add(child)
                    open_queue.put(Prio(f, child))


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
