from lib import Vector, Direction


def parse_input(input):
    return input.strip().splitlines()


def propagate(cell, d):
    match cell:
        case "|" if d.is_horizontal():
            yield Direction.NORTH
            yield Direction.SOUTH
        case "-" if d.is_vertical():
            yield Direction.EAST
            yield Direction.WEST
        case "/":
            yield d.turn_right() if d.is_vertical() else d.turn_left()
        case "\\":
            yield d.turn_left() if d.is_vertical() else d.turn_right()
        case _:
            yield d


def in_field(input, v):
    return 0 <= v.y < len(input) and 0 <= v.x < len(input[0])


def energized(input, v, d):
    visited = set()
    wave = {(v, d)}
    while len(wave):
        visited.update(wave)
        wave = set(
            (nv, nd)
            for v, d in wave
            for nd in propagate(input[v.y][v.x], d)
            if in_field(input, nv := v + nd.value) and (nv, nd) not in visited
        )
    return len(set(v for v, _ in visited))


def part1(input):
    return energized(input, Vector(0, 0), Direction.EAST)


def part2(input):
    maxy = len(input) - 1
    maxx = len(input[0]) - 1
    start = [
        *[(Vector(x, 0), Direction.SOUTH) for x in range(maxx + 1)],
        *[(Vector(x, maxy), Direction.NORTH) for x in range(maxx + 1)],
        *[(Vector(0, y), Direction.EAST) for y in range(maxy + 1)],
        *[(Vector(maxx, y), Direction.WEST) for y in range(maxy + 1)],
    ]
    return max(energized(input, v, d) for v, d in start)


def main():
    with open("../input/day_16.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 46


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 51
