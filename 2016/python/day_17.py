import hashlib
from functools import partial

from astar import astar


START = ((0, 0), ())
VAULT = (3, 3)


def parse_input(input):
    return input.strip()


def is_valid(pos):
    x, y = pos
    return x >= 0 and x <= 3 and y >= 0 and y <= 3


def neighbors(pos):
    x, y = pos
    return [("U", (x, y - 1)), ("D", (x, y + 1)), ("L", (x - 1, y)), ("R", (x + 1, y))]


def is_door_open(ch):
    return ch in "bcdef"


def adjacent(passcode, node):
    pos, path = node
    hash = hashlib.md5(bytes(f"{passcode}{''.join(path)}", "utf-8")).hexdigest()
    for (dir, pos), open in zip(neighbors(pos), map(is_door_open, hash[0:4])):
        if is_valid(pos) and open:
            yield 1, (pos, tuple(list(path) + [dir]))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part1(input):
    h = lambda node: manhattan(node[0], VAULT)
    is_target = lambda node: node[0] == VAULT
    adj = partial(adjacent, input)
    return "".join(astar(START, adj, h, is_target)[-1][1])


def part2(input):
    queue = set([START])
    longest = None
    while queue:
        node = queue.pop()
        for _, n in adjacent(input, node):
            if n[0] == VAULT:
                if longest is None or len(n[1]) > longest:
                    longest = len(n[1])
            else:
                queue.add(n)
    return longest


def main():
    with open("../input/day_17.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1("ihgpwlah") == "DDRRRD"
    assert part1("kglvqrro") == "DDUDRLRRUDRD"
    assert part1("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"


def test_part2():
    assert part2("ihgpwlah") == 370
    assert part2("kglvqrro") == 492
    assert part2("ulqzkmiv") == 830
