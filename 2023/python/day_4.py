import re


def parse_card(line):
    numbers = [
        list(map(int, re.split(r"\s+", m.group().strip())))
        for m in re.finditer(r"(\s+\d+)+", line)
    ]
    return numbers[0][0], set(numbers[1]), set(numbers[2])


def parse_input(input):
    return [parse_card(line) for line in input.strip().splitlines()]


def score(_, winning, mine):
    if count := len(mine.intersection(winning)):
        return 2 ** (count - 1)
    else:
        return 0


def part1(input):
    return sum(score(*card) for card in input)


def part2(input):
    queue = list(input)
    count = 0
    while queue:
        id, winning, mine = queue.pop()
        count += 1
        for i, _ in enumerate(mine.intersection(winning)):
            queue.append(input[id + i])
    return count


def main():
    with open("../input/day_4.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 13


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 30
