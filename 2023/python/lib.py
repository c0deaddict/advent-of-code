from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def add(self, o: "Vector") -> "Vector":
        return Vector(self.x + o.x, self.y + o.y)


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
