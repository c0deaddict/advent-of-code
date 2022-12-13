import operator
from functools import cmp_to_key, reduce
from itertools import chain


def parse_pair(pair):
    a, b = pair.splitlines()
    return eval(a), eval(b)


def parse_input(input):
    return [parse_pair(pair) for pair in input.strip().split("\n\n")]


def compare(left, right):
    match left, right:
        case int(l), int(r):
            return l - r
        case list(l), list(r):
            for i, a in enumerate(l):
                if len(r) < i + 1:
                    return 1
                d = compare(a, r[i])
                if d != 0:
                    return d
            return len(l) - len(r)
        case list(l), int(r):
            return compare(l, [r])
        case int(l), list(r):
            return compare([l], r)


def part1(input):
    return sum(i for i, pair in enumerate(input, start=1) if compare(*pair) < 0)


def part2(input):
    dividers = [[[2]], [[6]]]
    packets = list(chain(*input)) + dividers
    ordered = sorted(packets, key=cmp_to_key(compare))
    indices = (i for i, p in enumerate(ordered, start=1) if p in dividers)
    return reduce(operator.mul, indices, 1)


def main():
    with open("../input/day_13.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 13


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 140
