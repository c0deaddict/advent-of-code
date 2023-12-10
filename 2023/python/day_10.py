from enum import Enum


class Dir(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def move(self, x, y):
        return (x + self.value[0], y + self.value[1])

    def vert(self):
        return self in [Dir.NORTH, Dir.SOUTH]

    def horz(self):
        return self in [Dir.EAST, Dir.WEST]

    @staticmethod
    def get(a, b):
        return next(d for d in Dir if d.value == (b[0] - a[0], b[1] - a[1]))


def neighbors(cell):
    match cell:
        case "|":
            return {Dir.NORTH, Dir.SOUTH}
        case "-":
            return {Dir.EAST, Dir.WEST}
        case "L":
            return {Dir.NORTH, Dir.EAST}
        case "J":
            return {Dir.NORTH, Dir.WEST}
        case "7":
            return {Dir.SOUTH, Dir.WEST}
        case "F":
            return {Dir.SOUTH, Dir.EAST}
        case "S":
            return {Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST}
        case _:
            return {}


def edges(cell, v):
    return {d.move(*v) for d in neighbors(cell)}


def parse_input(input):
    return {
        (x, y): cell
        for y, row in enumerate(input.strip().splitlines())
        for x, cell in enumerate(row)
    }


def find_loop(input):
    start = next(pos for pos, cell in input.items() if cell == "S")
    g = {pos: edges(cell, pos) for pos, cell in input.items()}
    for v in g[start]:
        if v not in g or start not in g[v]:
            continue  # not connected.
        visited = set([v])
        path = [v]
        p = start  # remember the previous node, we don't want to go back.
        while True:
            n = next(n for n in g[v] if n not in visited and n != p)
            if v not in g[n]:
                break  # not connected
            visited.add(n)
            path.append(n)
            if n == start:
                return path
            p = v
            v = n
    return []


def part1(input):
    return (len(find_loop(input)) + 1) // 2


def print_map(g, loop, enclosed):
    minx = min(x for x, _ in g.keys())
    miny = min(y for _, y in g.keys())
    maxx = max(x for x, _ in g.keys())
    maxy = max(y for _, y in g.keys())
    print()
    for y in range(miny, maxy + 1):
        line = ""
        for x in range(minx, maxx + 1):
            p = (x, y)
            if p in enclosed:
                line += "I"
            elif p in loop:
                line += g[p]
            elif g[p] != ".":
                line += "."
            else:
                line += "."
        print(line)


def fix_start(loop):
    match Dir.get(loop[-1], loop[0]), Dir.get(loop[-1], loop[-2]):
        case (Dir.SOUTH, Dir.EAST) | (Dir.EAST, Dir.SOUTH):
            return "F"
        case (Dir.SOUTH, Dir.WEST) | (Dir.WEST, Dir.SOUTH):
            return "7"
        case (Dir.NORTH, Dir.EAST) | (Dir.EAST, Dir.NORTH):
            return "L"
        case (Dir.NORTH, Dir.WEST) | (Dir.WEST, Dir.NORTH):
            return "J"
        case (Dir.SOUTH | Dir.NORTH), _:
            return "|"
        case _:
            return "-"


def trace(g, loop, v, d):
    last_turn = None
    while True:
        v = d.move(*v)
        if v not in g:
            return False  # edge
        if v in loop:
            if g[v] == "|" and d.horz():
                return True
            elif g[v] == "-" and d.vert():
                return True
            elif g[v] not in ["|", "-"]:
                match last_turn, g[v], d:
                    case "F", "J", (Dir.EAST | Dir.SOUTH):
                        return True
                    case "J", "F", (Dir.WEST | Dir.NORTH):
                        return True
                    case "7", "L", (Dir.WEST | Dir.SOUTH):
                        return True
                    case "L", "7", (Dir.EAST | Dir.NORTH):
                        return True
                last_turn = g[v]


def scan(g, loop, v):
    wave = [v]
    result = set()
    while wave:
        result.update(wave)
        wave = set(
            n
            for v in wave
            for d in Dir
            if (n := d.move(*v)) in g and n not in loop and n not in result
        )
    return result


def enclosed(g, loop):
    visited = set()
    result = set()
    for v in g:
        if v not in loop and v not in visited:
            area = scan(g, loop, v)
            visited.update(area)
            if all(all(trace(g, loop, v, d) for d in Dir) for v in area):
                result.update(area)
    return result


def part2(input):
    loop = find_loop(input)
    input[loop[-1]] = fix_start(loop)
    print("fixed start", input[loop[-1]])
    loop = set(loop)
    e = enclosed(input, loop)
    print_map(input, loop, e)
    return len(e)


def main():
    with open("../input/day_10.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

EXAMPLE_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""


def test_part1_example1():
    assert part1(parse_input(EXAMPLE_1)) == 4


def test_part1_example2():
    assert part1(parse_input(EXAMPLE_2)) == 8


EXAMPLE_3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

EXAMPLE_4 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""

EXAMPLE_5 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""


EXAMPLE_6 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def test_part2_example3():
    assert part2(parse_input(EXAMPLE_3)) == 4


def test_part2_example4():
    assert part2(parse_input(EXAMPLE_4)) == 4


def test_part2_example5():
    assert part2(parse_input(EXAMPLE_5)) == 8


def test_part2_example6():
    assert part2(parse_input(EXAMPLE_6)) == 10
