import pytest
from collections import namedtuple
import operator
from functools import reduce


def parse_input(input):
    return dict(
        ((x, y), ch)
        for (y, line) in enumerate(input.strip().splitlines())
        for (x, ch) in enumerate(line.strip())
    )


def neighbours(point):
    x, y = point
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def part1(input):
    return 0


def part2(input):
    return 0


def main():
    with open("../input/day_18.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1_example1():
    input = """
#########
#b.A.@.a#
#########
"""
    print(input)
    assert part1(parse_input(input)) == 8


def test_part1_example2():
    input = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""
    print(input)
    assert part1(parse_input(input)) == 86


def test_part1_example3():
    input = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""
    print(input)
    assert part1(parse_input(input)) == 132


def test_part1_example4():
    input = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
    print(input)
    assert part1(parse_input(input)) == 136


def test_part1_example5():
    input = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""
    print(input)
    assert part1(parse_input(input)) == 81


def test_part2():
    assert False
