def parse_input(input):
    return [[int(s) for s in line.split()] for line in input.strip().splitlines()]


def is_triangle(l):
    [a, b, c] = l
    return a + b > c and b + c > a and a + c > b


def part1(input):
    return len(list(filter(is_triangle, input)))


def transform(input):
    for i in range(0, len(input), 3):
        for j in range(0, 3):
            yield [input[i + k][j] for k in range(0, 3)]


def part2(input):
    return len(list(filter(is_triangle, transform(input))))


def main():
    with open("../input/day_3.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert not is_triangle([5, 10, 25])


EXAMPLE_PART_2 = """
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
"""


def test_part2():
    assert list(transform(parse_input(EXAMPLE_PART_2))) == [
        [101, 102, 103],
        [301, 302, 303],
        [501, 502, 503],
        [201, 202, 203],
        [401, 402, 403],
        [601, 602, 603],
    ]
