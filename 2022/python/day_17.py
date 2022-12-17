from dataclasses import dataclass, field
from typing import Optional


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Rock:
    points: set[Point]

    @staticmethod
    def from_xy(*coords) -> "Rock":
        return Rock(set(map(lambda c: Point(*c), coords)))

    def at_position(self, pos: Point) -> set[Point]:
        return set(p + pos for p in self.points)

    def height(self) -> int:
        return max(p.y for p in self.points) + 1


@dataclass
class Field:
    width: int
    height: int = 0
    rocks: set[Point] = field(default_factory=set)

    def collide(self, rock: Rock, pos: Point) -> bool:
        return any(
            p.x < 0 or p.x >= self.width or p.y < 0 or p in self.rocks
            for p in rock.at_position(pos)
        )

    def add_rock(self, rock: Rock, pos: Point):
        for p in rock.at_position(pos):
            if p.y >= self.height:
                self.height = p.y + 1
            self.rocks.add(p)

    def print(self, rock: Optional[Rock] = None, pos: Optional[Point] = None):
        print()

        height = self.height
        falling_rock = set()
        if rock and pos:
            falling_rock = rock.at_position(pos)
            height = max(self.height, max(p.y for p in falling_rock))

        for y in range(height, -1, -1):
            line = "|"
            for x in range(0, self.width):
                if Point(x, y) in self.rocks:
                    line += "#"
                elif Point(x, y) in falling_rock:
                    line += "@"
                else:
                    line += "."
            line += "|"
            print(line)
        print("+" + "-" * self.width + "+")


ROCKS = [
    # -
    Rock.from_xy((0, 0), (1, 0), (2, 0), (3, 0)),
    # +
    Rock.from_xy((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    # inverted L
    Rock.from_xy((2, 2), (2, 1), (2, 0), (1, 0), (0, 0)),
    # i
    Rock.from_xy((0, 0), (0, 1), (0, 2), (0, 3)),
    # block
    Rock.from_xy((0, 0), (1, 0), (0, 1), (1, 1)),
]

DOWN = Point(0, -1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)


def parse_input(input):
    return input.strip()


def run(input, next_rock=0, next_jet=0):
    field = Field(width=7)

    while True:
        rock = ROCKS[next_rock]
        next_rock = (next_rock + 1) % len(ROCKS)
        pos = Point(2, field.height + 3)

        # print("\033c", end="")
        # field.print(rock, pos)
        # sleep(0.1)

        while True:
            # Try a push from the jetstream
            move = LEFT if input[next_jet] == "<" else RIGHT
            next_jet = (next_jet + 1) % len(input)
            if not field.collide(rock, pos + move):
                pos += move

            # Fall down.
            if field.collide(rock, pos + DOWN):
                field.add_rock(rock, pos)
                break
            pos += DOWN

        yield field, next_rock, next_jet


def nth(gen, n):
    for _ in range(n - 1):
        next(gen)
    return next(gen)


def part1(input):
    return nth(run(input), 2022)[0].height


def find_repetition(input):
    prev = {}
    for i, (field, next_rock, next_jet) in enumerate(run(input)):
        top = tuple(
            Point(x, field.height - 1) in field.rocks for x in range(field.width)
        )
        key = (top, next_rock, next_jet)
        if key in prev:
            return prev[key], (i, field.height)
        else:
            prev[key] = (i, field.height)


def part2(input):
    count = 1000000000000
    (start_offset, start_height), (end_offset, end_height) = find_repetition(input)

    # Start with height when repetition starts.
    count -= start_offset
    height = start_height

    # Compute the repetition.
    repeat = end_offset - start_offset
    height += (count // repeat) * (end_height - start_height)
    count = count % repeat

    # Compute the remainder.
    height += nth(run(input), start_offset + count)[0].height - start_height
    return height


def main():
    with open("../input/day_17.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 3068


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 1514285714288
