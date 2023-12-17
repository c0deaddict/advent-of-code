from lib import Vector, Direction, astar
from functools import partial


def parse_input(input):
    return [[int(c) for c in line] for line in input.strip().splitlines()]


def is_valid(input, v: Vector):
    return 0 <= v.y < len(input) and 0 <= v.x < len(input[0])


def adjacent(input, ultra: bool, n: tuple[Vector, Direction, int]):
    v, d, straight = n
    neighbors = []

    if not ultra or straight >= 4:
        l = d.turn_left()
        neighbors.append((v + l.value, l, 1))
        r = d.turn_right()
        neighbors.append((v + r.value, r, 1))

    if straight < (3 if not ultra else 10):
        neighbors.append((v + d.value, d, straight + 1))

    for v, d, straight in neighbors:
        if is_valid(input, v):
            yield input[v.y][v.x], (v, d, straight)


def print_path(input, path):
    print()
    points = {v: d for v, d, _ in path}
    for y, line in enumerate(input):
        out = ""
        for x, heat in enumerate(line):
            match points.get(Vector(x, y)):
                case Direction.NORTH:
                    c = "^"
                case Direction.EAST:
                    c = ">"
                case Direction.SOUTH:
                    c = "v"
                case Direction.WEST:
                    c = "<"
                case _:
                    c = str(heat)
            out += c
        print(out)


def shortest_path(input, ultra):
    start = (Vector(0, 0), Direction.EAST, 1)
    end = Vector(len(input) - 1, len(input[0]) - 1)
    is_target = lambda n: n[0] == end and (not ultra or n[2] >= 4)
    adj = partial(adjacent, input, ultra)
    h = lambda n: n[0].manhattan(end)
    path = astar(start, adj, h, is_target)
    # print_path(input, path)
    return sum(input[v.y][v.x] for v, _, _ in path[1:])


def part1(input):
    return shortest_path(input, False)


def part2(input):
    return shortest_path(input, True)


def main():
    with open("../input/day_17.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


EXAMPLE_2 = """
111111111111
999999999991
999999999991
999999999991
999999999991
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 102


def test_part2_example1():
    assert part2(parse_input(EXAMPLE_1)) == 94


def test_part2_example2():
    assert part2(parse_input(EXAMPLE_2)) == 71
