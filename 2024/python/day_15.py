from dataclasses import dataclass
from typing import Iterator
from copy import deepcopy

from lib import Vector, Direction


Warehouse = list[list[str]]


@dataclass
class Input:
    warehouse: Warehouse
    moves: str


MOVES = {
    "^": Direction.NORTH,
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
}


def parse_input(input: str):
    warehouse, moves = input.strip().split("\n\n")
    warehouse = [list(line.strip()) for line in warehouse.splitlines()]
    moves = "".join(moves.split())
    return Input(warehouse, moves)


def find_robot(warehouse: Warehouse) -> Vector:
    for y, line in enumerate(warehouse):
        for x, ch in enumerate(line):
            if ch == "@":
                return Vector(x, y)
    assert False


def find_boxes(warehouse: Warehouse) -> Iterator[Vector]:
    for y, line in enumerate(warehouse):
        for x, ch in enumerate(line):
            if ch == "O":
                yield Vector(x, y)


def gps(box: Vector) -> int:
    return box.y * 100 + box.x


def try_push_box(w: Warehouse, p: Vector, d: Direction) -> bool:
    assert w[p.y][p.x] == "O"
    t = p + d.value
    match w[t.y][t.x]:
        case "#":
            return False
        case "O":
            if not try_push_box(w, t, d):
                return False
    assert w[t.y][t.x] == "."
    w[t.y][t.x] = "O"
    w[p.y][p.x] = "."
    return True


def print_warehouse(w: Warehouse, robot: Vector):
    for y, line in enumerate(w):
        l = list(line)
        if y == robot.y:
            l[robot.x] = "@"
        print("".join(l))
    print()


def part1(input):
    warehouse = deepcopy(input.warehouse)
    robot = find_robot(warehouse)
    warehouse[robot.y][robot.x] = "."
    for move in input.moves:
        d = MOVES[move]
        p = robot + d.value
        match warehouse[p.y][p.x]:
            case ".":
                robot = p
            case "O":
                if try_push_box(warehouse, p, d):
                    robot = p
    return sum(map(gps, find_boxes(warehouse)))


def widen_cell(cell: str):
    match cell:
        case "#":
            return "##"
        case "O":
            return "[]"
        case ".":
            return ".."
        case "@":
            return "@."
        case _:
            assert False


def widen_warehouse(warehouse: Warehouse) -> Warehouse:
    return [[ch for cell in line for ch in widen_cell(cell)] for line in warehouse]


def find_big_boxes(warehouse: Warehouse) -> Iterator[Vector]:
    for y, line in enumerate(warehouse):
        for x, ch in enumerate(line):
            if ch == "[":
                yield Vector(x, y)


def try_push_big_box_horizontal(w: Warehouse, p: Vector, d: Direction) -> bool:
    t = p + d.value
    match w[t.y][t.x]:
        case "#":
            return False
        case "[" | "]":
            if not try_push_big_box_horizontal(w, t, d):
                return False
    assert w[t.y][t.x] == "."
    w[t.y][t.x] = w[p.y][p.x]
    w[p.y][p.x] = "."
    return True


def try_push_big_box_vertical(
    w: Warehouse,
    d: Direction,
    y: int,
    xs: list[int],
) -> bool:
    ty = y + d.value.y

    # if any in xs is a wall, don't move.
    if any(w[ty][x] == "#" for x in xs):
        return False

    # if line above is not entirely empty, recursively push boxes.
    if not all(w[ty][x] == "." for x in xs):
        nxs = [x for x in xs if w[ty][x] != "."]
        if w[ty][nxs[0]] == "]":
            nxs.insert(0, nxs[0] - 1)
        if w[ty][nxs[-1]] == "[":
            nxs.append(nxs[-1] + 1)
        if not try_push_big_box_vertical(w, d, ty, nxs):
            return False

    for x in xs:
        assert w[ty][x] == "."
        w[ty][x] = w[y][x]
        w[y][x] = "."

    return True


def try_push_big_box(w: Warehouse, p: Vector, d: Direction) -> bool:
    if d.is_horizontal():
        return try_push_big_box_horizontal(w, p, d)
    else:
        xs = [p.x - 1, p.x] if w[p.y][p.x] == "]" else [p.x, p.x + 1]
        return try_push_big_box_vertical(w, d, p.y, xs)


def part2(input):
    warehouse = widen_warehouse(input.warehouse)
    robot = find_robot(warehouse)
    warehouse[robot.y][robot.x] = "."
    for move in input.moves:
        d = MOVES[move]
        p = robot + d.value
        match warehouse[p.y][p.x]:
            case ".":
                robot = p
            case "[" | "]":
                if try_push_big_box(warehouse, p, d):
                    robot = p
    return sum(map(gps, find_big_boxes(warehouse)))


def main():
    with open("../input/day_15.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

EXAMPLE_2 = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 10092


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 9021
    assert part2(parse_input(EXAMPLE_2)) == 618
