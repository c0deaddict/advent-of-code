#!/usr/bin/env python3
import pytest
from collections import namedtuple
from itertools import permutations

Entry = namedtuple('Entry', 'digits output')

SEGMENTS = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg"
]

def parse_input(input):
    return [
        Entry(*[part.split() for part in line.split(" | ", 2)])
        for line in input.strip().splitlines()
    ]

def part1(input):
    unique_len = {2: 1, 3: 1, 4: 1, 7: 1}
    return sum(unique_len.get(len(s), 0) for e in input for s in e.output)

def map_digit(digit, order):
    return "".join(sorted(order[ord(c) - ord('a')] for c in digit))

def is_valid_order(entry, order):
    for d in entry.digits:
        if map_digit(d, order) not in SEGMENTS:
            return False
    return True

def find_order(entry):
    for order in permutations("abcdefg", 7):
        if is_valid_order(entry, order):
            return order
    return None

def compute_output(entry, order):
    return int("".join(
        str(SEGMENTS.index(map_digit(d, order)))
        for d in entry.output
    ))

def part2(input):
    return sum(compute_output(e, find_order(e)) for e in input)

def main():
    with open("../input/day_08.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))

if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 26

def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_1)) == 61229
