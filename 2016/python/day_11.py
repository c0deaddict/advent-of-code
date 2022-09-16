import re
from itertools import chain, combinations
from copy import deepcopy

from astar import astar


DEBUG = False


def parse_line(floor, line):
    m = re.match(rf"^The {floor} floor contains ([^\.]+)\.$", line)
    parts = m.group(1)
    items = set()
    if parts != "nothing relevant":
        items.update(("generator", g) for g in re.findall(r"(\w+) generator", parts))
        items.update(
            ("microchip", m) for m in re.findall(r"(\w+)-compatible microchip", parts)
        )
    return frozenset(items)


def parse_input(input):
    return tuple(
        parse_line(floor, line)
        for line, floor in zip(
            input.strip().splitlines(), ["first", "second", "third", "fourth"]
        )
    )


def items_safe_on_floor(items):
    # microchip can't be on a floor (without it's rtg) with other rtg's
    queue = set(items)
    count = 0
    for item in items:
        if item[0] == "generator":
            count += 1
            queue.remove(item)
            microchip = ("microchip", item[1])
            if microchip in queue:
                queue.remove(microchip)
    return count == 0 or len(queue) == 0


def unfreeze_state(state):
    return [set(items) for items in state]


def freeze_state(state):
    return tuple(map(frozenset, state))


def adjacent(node):
    floor, state = node

    next_floors = []
    if floor < 3:
        next_floors.append(floor + 1)
    if floor > 0:
        next_floors.append(floor - 1)

    # Take one or two items.
    choices = [set([item]) for item in state[floor]] + list(
        map(set, combinations(state[floor], 2))
    )
    for next_floor in next_floors:
        for choice in choices:
            if items_safe_on_floor(state[next_floor] | choice) and items_safe_on_floor(
                state[floor] - choice
            ):
                next_state = unfreeze_state(state)
                for item in choice:
                    next_state[floor].remove(item)
                    next_state[next_floor].add(item)
                yield 1, (next_floor, freeze_state(next_state))


def print_path(path, all_items):
    print()
    for floor, state in path:
        for i in range(4, 0, -1):
            line = f"F{i} {'E' if floor == i - 1 else '.'} "
            for item in sorted(all_items):
                if item in state[i - 1]:
                    line += f"{item[0][0]}{item[1][0:2]} "
                else:
                    line += ".   "
            print(line)
        print()


def part1(input):
    # Elevator starts on the first floor.
    start = (0, input)
    # Target: everything in assembling machine on fourth floor.
    all_items = set(chain(*input))
    is_target = lambda node: node[0] == 3 and node[1][3] == all_items
    h = lambda node: (3 - node[0]) + len(node[1][3]) - len(all_items)
    path = astar(start, adjacent, h, is_target)

    if DEBUG:
        print_path(path, all_items)

    return len(path) - 1


def part2(input):
    state = unfreeze_state(input)
    state[0].update(
        {
            ("generator", "elerium"),
            ("microchip", "elerium"),
            ("generator", "dilithium"),
            ("microchip", "dilithium"),
        },
    )
    return part1(freeze_state(state))


def main():
    with open("../input/day_11.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 11


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) is None
