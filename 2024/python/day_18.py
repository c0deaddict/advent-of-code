from lib import Vector, astar


def parse_input(input):
    return [
        Vector(*map(int, line.split(",", 2))) for line in input.strip().splitlines()
    ]


def find_path(input, size, n):
    corrupted = set(input[:n])
    start = Vector(0, 0)
    finish = Vector(size, size)

    h = lambda _: 1
    is_target = lambda n: n == finish

    def adjacent(n):
        return [
            (1, n)
            for n in n.neighbors()
            if n not in corrupted and 0 <= n.x <= size and 0 <= n.y <= size
        ]

    return astar(start, adjacent, h, is_target)


def part1(input, size=70, n=1024):
    cost, _ = find_path(input, size, n)
    return cost - 1


def part2(input, size=70, start=1024):
    path = None
    for n in range(start, len(input)):
        corrupted = input[n - 1]
        if path is None or corrupted in path:
            try:
                _, path = find_path(input, size, n)
            except:
                p = input[n - 1]
                return f"{p.x},{p.y}"


def main():
    with open("../input/day_18.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1), 6, 12) == 22


def test_part2():
    assert part2(parse_input(EXAMPLE_1), 6, 0) == "6,1"
