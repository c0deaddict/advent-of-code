from functools import partial


def parse_input(input):
    return [list(line) for line in input.strip().splitlines()]


def tilt_v(dy, m):
    result = [["." for _ in row] for row in m]
    height = [0] * len(m[0])
    f = lambda y: y if dy == -1 else len(m) - y - 1
    for y in range(len(m)):
        for x, cell in enumerate(m[f(y)]):
            match cell:
                case "O":
                    result[f(height[x])][x] = "O"
                    height[x] += 1
                case "#":
                    result[f(y)][x] = "#"
                    height[x] = y + 1
    return result


def tilt_h(dx, m):
    result = [["." for _ in row] for row in m]
    height = [0] * len(m)
    f = lambda x: x if dx == -1 else len(m[0]) - x - 1
    for x in range(len(m[0])):
        for y in range(len(m)):
            match m[y][f(x)]:
                case "O":
                    result[y][f(height[y])] = "O"
                    height[y] += 1
                case "#":
                    result[y][f(x)] = "#"
                    height[y] = x + 1
    return result


def load(m):
    return sum(
        len(m) - y
        for y, row in enumerate(m)
        for _, cell in enumerate(row)
        if cell == "O"
    )


def part1(input):
    return load(tilt_v(-1, input))


def cycle(m):
    for f in [
        partial(tilt_v, -1),  # north
        partial(tilt_h, -1),  # west
        partial(tilt_v, 1),  # south
        partial(tilt_h, 1),  # east
    ]:
        m = f(m)
    return m


def find_loop(m, count):
    loop = {}
    for i in range(count):
        m = cycle(m)
        key = "".join("".join(row) for row in m)
        if j := loop.get(key):
            # loop found from j to i
            return m, count - i - 1, i - j
        loop[key] = i
    assert False, "unreachable"


def run_cycles(m, count):
    m, count, loop = find_loop(m, count)
    for _ in range(count % loop):
        m = cycle(m)
    return m


def part2(input):
    return load(run_cycles(input, 1000000000))


def main():
    with open("../input/day_14.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


EXAMPLE_1_CYCLE_1 = """
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
"""

EXAMPLE_1_CYCLE_2 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 136


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 64


def test_cycle():
    assert cycle(parse_input(EXAMPLE_1)) == parse_input(EXAMPLE_1_CYCLE_1)
    assert cycle(cycle(parse_input(EXAMPLE_1))) == parse_input(EXAMPLE_1_CYCLE_2)
