def parse_input(input):
    return [line.strip() for line in input.strip().split("\n")]


KEYPAD_PART1 = {
    (0, 0): "1",
    (1, 0): "2",
    (2, 0): "3",
    (0, 1): "4",
    (1, 1): "5",
    (2, 1): "6",
    (0, 2): "7",
    (1, 2): "8",
    (2, 2): "9",
}


def goto(pos, ch):
    x, y = pos
    if ch == "U":
        return (x, y - 1)
    elif ch == "D":
        return (x, y + 1)
    elif ch == "L":
        return (x - 1, y)
    elif ch == "R":
        return (x + 1, y)


def code(input, keypad, start):
    pos = start
    result = ""
    for line in input:
        for ch in line:
            next = goto(pos, ch)
            if next in keypad.keys():
                pos = next
        result += keypad[pos]
    return result


def part1(input):
    return code(input, KEYPAD_PART1, (1, 1))


KEYPAD_PART2 = {
    (0, -2): "1",
    (-1, -1): "2",
    (0, -1): "3",
    (1, -1): "4",
    (-2, 0): "5",
    (-1, 0): "6",
    (0, 0): "7",
    (1, 0): "8",
    (2, 0): "9",
    (-1, 1): "A",
    (0, 1): "B",
    (1, 1): "C",
    (0, 2): "D",
}


def part2(input):
    return code(input, KEYPAD_PART2, (-2, 0))


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
ULL
RRDDD
LURDL
UUUUD
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == "1985"


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == "5DB3"
