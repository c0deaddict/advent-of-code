def parse_input(input):
    fresh, available = input.strip().split("\n\n")
    fresh = [list(map(int, line.split("-", 2))) for line in fresh.strip().splitlines()]
    available = list(map(int, available.strip().splitlines()))
    return fresh, available


def part1(input):
    fresh, available = input
    return sum(
        1
        for id in available
        if any(id >= start and id <= stop for start, stop in fresh)
    )


def overlap(a, b):
    return not a[1] < b[0] and not b[1] < a[0]


def part2(input):
    fresh, _ = input
    distinct = []
    queue = list(fresh)
    while queue:
        a = queue.pop()
        for b in distinct:
            if overlap(a, b):
                queue.append((min(a[0], b[0]), max(a[1], b[1])))
                distinct.remove(b)
                break
        else:
            distinct.append(a)
    return sum(stop - start + 1 for start, stop in distinct)


def main():
    with open("../input/day_5.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 3


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 14
