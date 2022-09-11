from collections import Counter
from operator import itemgetter


def parse_input(input):
    return input.strip().splitlines()


def frequencies(seq):
    return Counter(seq).items()


def columns(input):
    return ([row[i] for row in input] for i, _ in enumerate(input[0]))


def part1(input):
    return "".join(
        max(frequencies(col), key=itemgetter(1))[0] for col in columns(input)
    )


def part2(input):
    return "".join(
        min(frequencies(col), key=itemgetter(1))[0] for col in columns(input)
    )


def main():
    with open("../input/day_6.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == "easter"


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == "advent"
