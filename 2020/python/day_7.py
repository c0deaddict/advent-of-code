import re
from collections import defaultdict


def parse_rule(line):
    left, right = line.split("bags contain")
    return left.strip(), [
        (int(m[1]), m[2]) for m in re.finditer(r"(\d+) (\w+ \w+) bags?", right)
    ]


def parse_input(input):
    return list(map(parse_rule, input.strip().splitlines()))


def part1(input):
    parents = defaultdict(list)
    for parent, children in input:
        for _count, child in children:
            parents[child].append(parent)

    result = 0
    queue = ["shiny gold"]
    visited = set()
    while queue:
        bag = queue.pop()
        for parent in parents[bag]:
            if parent not in visited:
                visited.add(parent)
                queue.append(parent)
                result += 1

    return result


def count_bags(graph, bag):
    result = 1
    for count, child in graph[bag]:
        result += count * count_bags(graph, child)
    return result


def part2(input):
    return count_bags(dict(input), "shiny gold") - 1


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 4


def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_1)) == 32
