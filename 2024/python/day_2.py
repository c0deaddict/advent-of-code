def parse_input(input):
    return [[int(d) for d in line.split()] for line in input.strip().splitlines()]


def sign(i):
    return i / abs(i)


def is_safe(report):
    s = None
    for i in range(len(report) - 1):
        d = report[i] - report[i + 1]
        if not (1 <= abs(d) <= 3):
            return False
        if i == 0:
            s = sign(d)
        elif sign(d) != s:
            return False
    return True


def part1(input):
    return sum(int(is_safe(report)) for report in input)


def problem_dampener(report):
    yield report
    for i in range(len(report)):
        other = list(report)
        other.pop(i)
        yield other


def part2(input):
    return sum(
        int(any(is_safe(r) for r in problem_dampener(report))) for report in input
    )


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 2


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 4
