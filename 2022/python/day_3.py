from functools import reduce


def parse_input(input):
    return input.strip().splitlines()


def priority(item):
    if item.islower():
        return ord(item) - ord("a") + 1
    else:
        return ord(item) - ord("A") + 27


def find_common(rucksack):
    a, b = rucksack[: len(rucksack) // 2], rucksack[len(rucksack) // 2 :]
    return set(a).intersection(set(b))


def part1(input):
    return sum(sum(map(priority, find_common(rs))) for rs in input)


def groups(input):
    for i in range(len(input) // 3):
        yield input[i * 3 : (i + 1) * 3]


def find_common_in_group(group):
    return reduce(set.intersection, map(set, group))


def part2(input):
    return sum(sum(map(priority, find_common_in_group(g))) for g in groups(input))


def main():
    with open("../input/day_3.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 157


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 70
