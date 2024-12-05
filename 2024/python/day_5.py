from functools import cmp_to_key
from dataclasses import dataclass

from lib import split_ints


@dataclass
class Input:
    rules: list[list[int]]
    updates: list[list[int]]


def parse_input(input) -> Input:
    rules, updates = input.split("\n\n")
    return Input(
        [split_ints(line, "|") for line in rules.strip().splitlines()],
        [split_ints(line, ",") for line in updates.strip().splitlines()],
    )


def fix_order(rules, update):
    rules = set((a, b) for a, b in rules)

    def compare(a, b):
        if (a, b) in rules:
            return -1
        elif (b, a) in rules:
            return 1
        else:
            return 0

    return sorted(update, key=cmp_to_key(compare))


def middle_page_number(update):
    return update[len(update) // 2]


def part1(input):
    return sum(
        middle_page_number(update)
        for update in input.updates
        if fix_order(input.rules, update) == update
    )


def part2(input):
    return sum(
        middle_page_number(fixed)
        for update in input.updates
        if (fixed := fix_order(input.rules, update)) != update
    )


def main():
    with open("../input/day_5.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 143


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 123
