from functools import reduce
import operator


def parse_input(input):
    return [int(line) for line in input.strip().splitlines()]


def product(it):
    return reduce(operator.mul, it)


def enumerate_groups(pkgs, size):
    def recurse(pkgs, group):
        if (s := sum(group)) == size:
            yield group
        if s > size or not pkgs:
            return
        yield from recurse(pkgs[1:], group + [pkgs[0]])
        yield from recurse(pkgs[1:], group)

    return recurse(pkgs, [])


def lowest_qe(it):
    return product(min(it, key=lambda g: (len(g), product(g))))


def part1(input):
    return lowest_qe(enumerate_groups(input, sum(input) // 3))


def part2(input):
    return lowest_qe(enumerate_groups(input, sum(input) // 4))


def main():
    with open("../input/day_24.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
1
2
3
4
5
7
8
9
10
11
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 99


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 44
