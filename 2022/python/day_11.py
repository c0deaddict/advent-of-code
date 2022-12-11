import re
from dataclasses import dataclass
from typing import Callable
from functools import reduce
from copy import deepcopy
import operator


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test_divisor: int
    if_true: int
    if_false: int
    items_inspected: int = 0


def find_ints(s):
    return list(map(int, re.findall(r"\d+", s)))


def parse_operation(s):
    m = re.search(r"new = old (\+|\*) (\d+|old)", s)

    def f(old):
        nonlocal m
        rhs = old if m.group(2) == "old" else int(m.group(2))
        if m.group(1) == "+":
            return old + rhs
        else:
            return old * rhs

    return f


def parse_monkey(id, input):
    [_, items, operation, test, if_true, if_false] = input.splitlines()
    items = find_ints(items)
    operation = parse_operation(operation)
    test_divisor = find_ints(test)[0]
    if_true = find_ints(if_true)[0]
    if_false = find_ints(if_false)[0]
    return Monkey(id, items, operation, test_divisor, if_true, if_false)


def parse_input(input):
    return [
        parse_monkey(i, chunk.strip())
        for i, chunk in enumerate(input.strip().split("\n\n"))
    ]


def round(monkeys, worry_divide):
    div = reduce(operator.mul, (m.test_divisor for m in monkeys), 1)

    for m in monkeys:
        while m.items:
            item = m.items.pop(0)
            item = m.operation(item)
            if worry_divide:
                item = item // 3
            else:
                item = item % div
            target = m.if_true if item % m.test_divisor == 0 else m.if_false
            monkeys[target].items.append(item)
            m.items_inspected += 1


def monkey_business(input):
    top = sorted(m.items_inspected for m in input)[-2:]
    return top[0] * top[1]


def part1(input):
    input = deepcopy(input)
    for _ in range(20):
        round(input, worry_divide=True)
    return monkey_business(input)


def part2(input):
    input = deepcopy(input)
    for i in range(10000):
        round(input, worry_divide=False)
    return monkey_business(input)


def main():
    with open("../input/day_11.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 10605


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 2713310158
