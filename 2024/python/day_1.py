import collections


def parse_input(input):
    lists = [[], []]
    for line in input.strip().splitlines():
        a, b = line.split()
        lists[0].append(int(a))
        lists[1].append(int(b))
    return lists


def part1(input):
    return sum(abs(a - b) for (a, b) in zip(sorted(input[0]), sorted(input[1])))


def part2(input):
    right = collections.Counter(input[1])
    return sum(left * right[left] for left in input[0])


def main():
    with open("../input/day_1.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 11


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 31
