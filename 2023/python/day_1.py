def parse_input(input):
    return input.strip().splitlines()


def first_and_last(digits):
    return 10 * digits[0] + digits[-1]


def part1(input):
    return sum(first_and_last([int(c) for c in line if c.isdigit()]) for line in input)


digit_strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def find_digit(s: str, forward: bool) -> int:
    i = 0 if forward else len(s) - 1
    while i >= 0 and i < len(s):
        if s[i].isdigit():
            return int(s[i])
        for j, d in enumerate(digit_strings):
            if s[i:].startswith(d):
                return j + 1
        i += 1 if forward else -1


def first_and_last_part2(line):
    first = find_digit(line, True)
    last = find_digit(line, False)
    return first * 10 + last


def part2(input):
    return sum(first_and_last_part2(line) for line in input)


def main():
    with open("../input/day_1.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 142


EXAMPLE_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def test_part2():
    assert first_and_last_part2("eight1two3abthreexy") == 83
    assert first_and_last_part2("6sixoneightnc") == 68
    assert part2(parse_input(EXAMPLE_2)) == 281
