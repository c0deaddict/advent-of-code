import re
from lib import Vector


def parse_input(input):
    return input.strip().splitlines()


def is_valid(m, v):
    return 0 <= v.x < len(m[0]) and 0 <= v.y < len(m)


def neighbors(m, v):
    left = Vector(v.x - 1, v.y)
    if is_valid(m, left) and m[left.y][left.x] in (".<"):
        yield left

    right = Vector(v.x + 1, v.y)
    if is_valid(m, right) and m[right.y][right.x] in (".>"):
        yield right

    up = Vector(v.x, v.y - 1)
    if is_valid(m, up) and m[up.y][up.x] in (".^"):
        yield up

    down = Vector(v.x, v.y + 1)
    if is_valid(m, down) and m[down.y][down.x] in (".v"):
        yield down


def end(m):
    return Vector(len(m[0])-2, len(m)-1)


def find_longest_path(m, start, path, cache):
    prefix = len(path)
    match cache.get(start):
        case (count, sub):
            if prefix > count:
                print("better path", prefix, count)
                return (prefix - count) + sub
            else:
                return sub
        case count if type(count) is int:
            return count

    v = start
    count = 1
    while True:
        path.add(v)
        match [n for n in neighbors(m, v) if n not in path]:
            case []:
                cache[start] = count if v == end(m) else 0
                return cache[start]
            case [n]:
                v = n
                count += 1
            case options:
                count += max(find_longest_path(m, n, set(path), cache) for n in options)
                cache[start] = (prefix, count)
                return count


def part1(input):
    return find_longest_path(input, Vector(1, 0), set(), {}) - 1


def part2(input):
    m = [re.sub(r"[<>v^]", ".", line) for line in input]
    return find_longest_path(m, Vector(1, 0), set(), {}) - 1


def main():
    with open("../input/day_23.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 94


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 154
