from copy import deepcopy


def parse_input(input):
    return [[list(row) for row in p.splitlines()] for p in input.strip().split("\n\n")]


def find_reflection(pattern, ignore):
    for i in range(len(pattern) - 1):
        if i + 1 != ignore and all(
            pattern[i - j] == pattern[i + 1 + j]
            for j in range(0, 1 + min(i, len(pattern) - 2 - i))
        ):
            return i + 1

    return None


def rotate(pattern):
    return [
        [pattern[len(pattern) - 1 - y][x] for y in range(len(pattern))]
        for x in range(len(pattern[0]))
    ]


def score_pattern(pattern, ignore=None):
    if i := find_reflection(pattern, ignore / 100 if ignore is not None else None):
        return 100 * i
    return find_reflection(rotate(pattern), ignore)


def part1(input):
    return sum(score_pattern(p) for p in input)


def fix_smudge(pattern):
    original = score_pattern(pattern)
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            p = deepcopy(pattern)
            p[y][x] = "." if p[y][x] == "#" else "#"
            score = score_pattern(p, original)
            if score is not None:
                return score


def part2(input):
    return sum(fix_smudge(p) for p in input)


def main():
    with open("../input/day_13.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

EXAMPLE_2 = """
....####.#####...
..##..###.##.##.#
..##..###.##.##.#
....####.#####...
.....#.####.#.#.#
###.#####.####...
##...#..##.#..###
##.....#.#.###...
..##.##..#..###..
####.#.#...#.##..
##.###..#.#....##
...##...#..##..#.
..#.####.##......
##.######....####
....#.#..#####...
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 405


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 400


def test_example2():
    assert score_pattern(parse_input(EXAMPLE_2)[0], 200) == 1
