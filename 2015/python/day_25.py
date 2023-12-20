import re


def parse_input(input):
    return tuple(map(int, re.findall(r"\d+", input)))


def part1(input):
    prev = 20151125
    paper = {}
    paper[(1, 1)] = prev
    d = 2
    while input not in paper:
        for i in range(d):
            prev = (prev * 252533) % 33554393
            paper[(d - i, 1 + i)] = prev
        d += 1
    return paper[input]


def part2(input):
    pass


def main():
    with open("../input/day_25.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()
