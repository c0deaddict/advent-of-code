import pytest


def parse_input(input):
    return input.strip()


def part1(input):
    sum = 0
    prev = input[-1]
    for digit in input:
        if digit == prev:
            sum += int(digit)
        prev = digit
    return sum


def part2(input):
    sum = 0
    lookahead = len(input) // 2
    for (index, digit) in enumerate(input):
        if digit == input[(index + lookahead) % len(input)]:
            sum += int(digit)
    return sum


def main():
    with open("../input/day_1.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1(parse_input("1122")) == 3
    assert part1(parse_input("1111")) == 4
    assert part1(parse_input("1234")) == 0
    assert part1(parse_input("91212129")) == 9


def test_part2():
    assert part2(parse_input("1212")) == 6
    assert part2(parse_input("1221")) == 0
    assert part2(parse_input("123425")) == 4
    assert part2(parse_input("123123")) == 12
    assert part2(parse_input("12131415")) == 4
