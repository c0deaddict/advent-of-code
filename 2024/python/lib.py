from enum import Enum
from dataclasses import dataclass
from astar import astar
from typing import Callable
import math
from typing import Any


def sign(i):
    if i == 0:
        return 0
    elif i < 0:
        return -1
    else:
        return 1


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, o: "Vector") -> "Vector":
        return Vector(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Vector") -> "Vector":
        return Vector(self.x - o.x, self.y - o.y)

    def __mul__(self, o: "Vector") -> "Vector":
        return Vector(self.x * o.x, self.y * o.y)

    def scale(self, c: int) -> "Vector":
        return Vector(self.x * c, self.y * c)

    def scale_gcd(self) -> "Vector":
        d = math.gcd(self.x, self.y)
        if d == 0:
            return self
        else:
            return Vector(self.x // d, self.y // d)

    def invert(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def sign(self) -> "Vector":
        return Vector(sign(self.x), sign(self.y))

    def manhattan(self, o: "Vector") -> int:
        return abs(self.x - o.x) + abs(self.y - o.y)

    def neighbors(self):
        return [
            Vector(self.x - 1, self.y),
            Vector(self.x + 1, self.y),
            Vector(self.x, self.y - 1),
            Vector(self.x, self.y + 1),
        ]

    def in_area(self, map: list[list[Any]]) -> bool:
        return 0 <= self.x < len(map[0]) and 0 <= self.y < len(map)

    def get(self, map: list[list[Any]]) -> Any | None:
        if self.in_area(map):
            return map[self.y][self.x]
        else:
            return None


class Direction(Enum):
    NORTH = Vector(0, -1)
    EAST = Vector(1, 0)
    SOUTH = Vector(0, 1)
    WEST = Vector(-1, 0)

    def is_vertical(self):
        return self.value.x == 0

    def is_horizontal(self):
        return self.value.y == 0

    def turn_right(self):
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH

    def turn_left(self):
        match self:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.NORTH

    @staticmethod
    def get(a: "Vector", b: "Vector"):
        return next(d for d in Direction if d.value == (b - a).sign())


def enclosed(path: list[Vector], outside: Callable[[Vector], bool]) -> set[Vector]:
    path_set = set(path)

    def scan(v, d):
        result = []
        while True:
            v += d.value
            if v in path_set:
                return result
            if outside(v):
                raise ValueError("not enclosed")
            result.append(v)

    def try_enclosed(turn: Callable[[Direction], Direction]):
        result = set()
        prev = None
        for a, b in zip(path, path[1:]):
            d = turn(Direction.get(a, b))
            # if turning: also cast normal in "open" part of the corner.
            if prev and d != prev and Direction.get(a, b) == prev:
                result.update(scan(a, prev))
            result.update(scan(a, d))
            prev = d
        return result

    try:
        return try_enclosed(Direction.turn_left)
    except ValueError:
        return try_enclosed(Direction.turn_right)


def split_ints(line, sep):
    return list(map(int, line.split(sep)))
