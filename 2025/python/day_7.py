def parse_input(input):
    return input.strip().splitlines()


def part1(input):
    start = input[0].index("S")
    beam = {start}
    splits = 0
    for y in range(1, len(input)):
        next_beam = set()
        for x in beam:
            if input[y][x] == "^":
                splits += 1
                next_beam.update({x - 1, x + 1})
            else:
                next_beam.add(x)
        beam = next_beam
    return splits


def part2(input):
    start = input[0].index("S")
    beam = {start: 1}
    for y in range(1, len(input)):
        next_beam = {}
        for x, count in beam.items():
            if input[y][x] == "^":
                next_beam[x - 1] = next_beam.get(x - 1, 0) + count
                next_beam[x + 1] = next_beam.get(x + 1, 0) + count
            else:
                next_beam[x] = next_beam.get(x, 0) + count
        beam = next_beam
    return sum(beam.values())


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 21


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 40
