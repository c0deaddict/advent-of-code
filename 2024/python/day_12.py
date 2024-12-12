from lib import Vector, Direction


def parse_input(input):
    return input.strip().splitlines()


def plots(input):
    for y, line in enumerate(input):
        for x, _ in enumerate(line):
            yield Vector(x, y)


def scan(input, v):
    plant = v.get(input)
    area = set()
    perimeter = set()
    wave = {v}
    while wave:
        area.update(wave)
        next_wave = set()
        for v in wave:
            for n in v.neighbors():
                if n in area:
                    continue
                if n.get(input) == plant:
                    next_wave.add(n)
                else:
                    perimeter.add((v, Direction.get(v, n)))
        wave = next_wave
    return area, perimeter


def part1(input):
    cost = 0
    visited = set()
    for v in plots(input):
        if v not in visited:
            area, perimeter = scan(input, v)
            visited.update(area)
            cost += len(area) * len(perimeter)
    return cost


def sides(perimeter):
    count = 0
    while perimeter:
        v, normal = perimeter.pop()
        count += 1

        # Scan to right and remove all neighbors with same normal.
        dr = normal.turn_right().value
        n = v
        while (n := n + dr, normal) in perimeter:
            perimeter.remove((n, normal))

        # Scan to left and remove all neighbors with same normal.
        dl = normal.turn_left().value
        n = v
        while (n := n + dl, normal) in perimeter:
            perimeter.remove((n, normal))

    return count


def part2(input):
    cost = 0
    visited = set()
    for v in plots(input):
        if v not in visited:
            area, perimeter = scan(input, v)
            visited.update(area)
            cost += len(area) * sides(perimeter)
    return cost


def main():
    with open("../input/day_12.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
AAAA
BBCD
BBCC
EEEC
"""

EXAMPLE_2 = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

EXAMPLE_3 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 140
    assert part1(parse_input(EXAMPLE_2)) == 772
    assert part1(parse_input(EXAMPLE_3)) == 1930


EXAMPLE_4 = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

EXAMPLE_5 = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 80
    assert part2(parse_input(EXAMPLE_2)) == 436
    assert part2(parse_input(EXAMPLE_3)) == 1206
    assert part2(parse_input(EXAMPLE_4)) == 236
    assert part2(parse_input(EXAMPLE_5)) == 368
