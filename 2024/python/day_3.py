import re


def parse_input(input):
    return input.strip()


def part1(input):
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d+),(\d+)\)", input))


def part2(input):
    enabled = True
    result = 0
    for m in re.finditer(r"do\(\)|don't\(\)|mul\((\d+),(\d+)\)", input):
        if m.group() == "do()":
            enabled = True
        elif m.group() == "don't()":
            enabled = False
        elif enabled:
            result += int(m.groups()[0]) * int(m.groups()[1])
    return result


def main():
    with open("../input/day_3.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 161


EXAMPLE_2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_2)) == 48
