import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Tuple, List
from copy import deepcopy
from functools import reduce
from itertools import chain


@dataclass
class Bot:
    values: List[int]
    low: Optional[Tuple[str, int]]
    high: Optional[Tuple[str, int]]


def parse_input(input):
    bots = defaultdict(lambda: Bot(values=[], low=None, high=None))
    for line in input.strip().splitlines():
        if m := re.match(r"^value (\d+) goes to bot (\d+)$", line):
            bots[("bot", m.group(2))].values.append(int(m.group(1)))
        else:
            m = re.match(
                r"^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$",
                line,
            )
            bot = bots[("bot", m.group(1))]
            bot.low = (m.group(2), m.group(3))
            bot.high = (m.group(4), m.group(5))
    return bots


def run(input):
    input = deepcopy(input)
    queue = [id for id, bot in input.items() if len(bot.values) == 2]
    while queue:
        bot = input[queue.pop()]
        a, b = sorted(bot.values)
        if input[bot.low].values:
            queue.append(bot.low)
        input[bot.low].values.append(a)
        if input[bot.high].values:
            queue.append(bot.high)
        input[bot.high].values.append(b)
    return input


def which_bot_compares(slots, a, b):
    return next(
        id for id, bot in slots.items() if bot.values == [a, b] or bot.values == [b, a]
    )


def part1(input):
    return which_bot_compares(run(input), 61, 17)[1]


def part2(input):
    return reduce(
        lambda x, y: x * y,
        chain(
            *(
                bot.values
                for id, bot in run(input).items()
                if id[0] == "output" and id[1] in ("0", "1", "2")
            )
        ),
    )


def main():
    with open("../input/day_10.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""


def test_part1():
    assert which_bot_compares(run(parse_input(EXAMPLE_1)), 5, 2) == ("bot", "2")
