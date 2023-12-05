import re
from dataclasses import dataclass
from operator import itemgetter


@dataclass(frozen=False)
class Almanac:
    seeds: list[int]
    maps: list[list[list[int]]]


def parse_ints(line):
    return [int(s) for s in re.findall(r"\d+", line)]


def parse_input(input) -> Almanac:
    blocks = input.strip().split("\n\n")
    return Almanac(
        seeds=parse_ints(blocks[0]),
        maps=[
            [parse_ints(line) for line in block.splitlines()[1:]]
            for block in blocks[1:]
        ],
    )


def part1(input):
    locations = []
    for seed in input.seeds:
        i = seed
        for m in input.maps:
            for dst_start, src_start, range_len in m:
                if i >= src_start and i < src_start + range_len:
                    i = dst_start + (i - src_start)
                    break
        locations.append(i)
    return min(locations)


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


def part2(input):
    ranges = list(grouper(input.seeds, 2))
    for m in input.maps:
        next_ranges = []
        for i, count in ranges:
            for dst_start, src_start, range_len in sorted(m, key=itemgetter(1)):
                if count != 0 and i >= src_start and i < src_start + range_len:
                    offset = i - src_start
                    slice_count = min(range_len - offset, count)
                    next_ranges.append((dst_start + offset, slice_count))
                    count -= slice_count
                    i = src_start + range_len
            if count != 0:
                next_ranges.append((i, count))
        ranges = next_ranges
    return min(start for start, _ in ranges)


def main():
    with open("../input/day_5.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 35


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 46
