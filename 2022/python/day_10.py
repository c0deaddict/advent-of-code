from itertools import count


def parse_input(input):
    return input.strip().splitlines()


def signal(input):
    x = 1
    for line in input:
        if line == "noop":
            yield x, x  # during and after
        elif line.startswith("addx"):
            yield x, x  # first cycle
            oldx = x
            x += int(line.split()[1])
            yield oldx, x  # x is changed after second cycle


def part1(input):
    result = 0
    # We're only interesting in the cycle *during* the cycle.
    for i, (x, _) in enumerate(signal(input), start=1):
        if i in [20, 60, 100, 140, 180, 220]:
            result += i * x
        if i == 220:
            return result


def part2(input):
    output = ""
    for i, (x, _) in enumerate(signal(input)):
        if i % 40 == 0:
            output += "\n"
        crt = i % 40
        output += "#" if crt >= x - 1 and crt <= x + 1 else "."
    return output


def main():
    with open("../input/day_10.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


def test_signal():
    assert list(signal(["noop", "addx 3", "addx -5"])) == [
        (1, 1),
        (1, 1),
        (1, 4),
        (4, 4),
        (4, -1),
    ]


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 13140


OUTPUT_1 = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == OUTPUT_1.rstrip()
