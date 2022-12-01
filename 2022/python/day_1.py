def parse_input(input):
    return [
        list(map(int, elf.strip().splitlines())) for elf in input.strip().split("\n\n")
    ]


def part1(input):
    return sum(max(input, key=sum))


def part2(input):
    return sum(map(sum, sorted(input, key=sum, reverse=True)[:3]))


def main():
    with open("../input/day_1.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 24000


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 45000
