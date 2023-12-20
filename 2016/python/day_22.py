import re
from dataclasses import dataclass

from astar import astar


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    size: int
    used: int


def parse_input(input):
    return {
        (n.x, n.y): n
        for line in input.strip().splitlines()[2:]
        if (n := Node(*[int(s) for s in re.findall(r"\d+", line)][0:4]))
    }


def part1(input):
    return sum(
        1
        for a in input.values()
        for b in input.values()
        if a != b and a.used > 0 and a.used <= b.size - b.used
    )


def neighbors(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def colored(color, s):
    return f"\033[{color}m{s}\033[0m"


def print_map(nodes, current, used, path=set()):
    print()
    maxx = max(n.x for n in nodes.values())
    maxy = max(n.y for n in nodes.values())
    for y in range(0, maxy + 1):
        line = []
        for x in range(0, maxx + 1):
            p = (x, y)
            n = nodes[p]
            full = used[p] / float(n.size)
            if p == current:
                line.append("G")
            elif p in path:
                line.append(colored(33, "P"))
            elif full < 0.2:
                line.append(colored(31, "E"))
            elif full < 0.8:
                line.append(".")
            else:
                line.append("#")
        print(" ".join(line))


def freeze_dict(d):
    return frozenset(sorted(d.items()))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(nodes, source, target, used, current):
    start = (target, used[target])

    def adjacent(v):
        target, target_used = v
        for source in neighbors(*target):
            if source not in nodes or source == current:
                continue
            if used[source] <= nodes[target].size - target_used:
                yield 1, (source, 0)

    h = lambda n: manhattan(n[0], source)
    is_target = lambda n: n[0] == source

    return astar(start, adjacent, h, is_target)


def part2(input):
    used = {p: n.used for p, n in input.items()}
    maxx = max(n.x for n in input.values())
    current = (maxx, 0)
    result = 0

    while current != (0, 0):
        source = (current[0] - 1, 0)
        path = min(
            (
                path
                for target, s in input.items()
                if target != source
                and any(
                    n in used and s.size - used[target] >= used[n]
                    for n in neighbors(*target)
                )
                and (path := find_path(input, source, target, used, current))
            ),
            key=len,
        )

        for (a, _), (b, _) in zip(path, path[1:]):
            used[a] += used[b]
            used[b] = 0

        used[source] += used[current]
        used[current] = 0

        current = source
        result += len(path)

    return result


def main():
    with open("../input/day_22.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 7
