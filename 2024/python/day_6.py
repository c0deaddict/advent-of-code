from dataclasses import dataclass

from lib import Vector, Direction


@dataclass
class Input:
    guard: Vector
    obstacles: set[Vector]
    width: int
    height: int


def parse_input(input):
    field = input.strip().splitlines()
    guard = None
    obstacles = set()
    for y, line in enumerate(field):
        for x, ch in enumerate(line):
            if ch == "^":
                guard = Vector(x, y)
            elif ch == "#":
                obstacles.add(Vector(x, y))
    assert guard is not None
    return Input(guard, obstacles, len(field[0]), len(field))


def in_area(input, p):
    return 0 <= p.x < input.width and 0 <= p.y < input.height


def trace_path(input, obstacles):
    guard = input.guard
    dir = Direction.NORTH
    visited = set()
    loop = False
    while True:
        if loop := (guard, dir) in visited:
            break
        visited.add((guard, dir))
        pos = guard + dir.value
        if not in_area(input, pos):
            break
        if pos in obstacles:
            dir = dir.turn_right()
        else:
            guard = pos
    return set(p for p, _ in visited), loop


def part1(input):
    visited, _ = trace_path(input, input.obstacles)
    return len(visited)


def part2(input):
    visited, _ = trace_path(input, input.obstacles)
    count = 0
    for p in visited:
        _, loop = trace_path(input, input.obstacles | {p})
        if loop:
            count += 1
    return count


def main():
    with open("../input/day_6.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 41


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 6
