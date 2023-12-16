def parse_line(line):
    parts = line.split(" ")
    return list(parts[0].strip()), list(map(int, parts[1].strip().split(",")))


def parse_input(input):
    return [parse_line(line) for line in input.strip().splitlines()]


def match_block(springs, size):
    block = springs[:size]
    if len(block) < size:
        return False
    if "." in block:
        return False
    if "#" in springs[size : size + 1]:
        return False
    return True


cache = {}


def arrangements(springs, counts):
    if len(counts) == 0:
        return 1 if "#" not in springs else 0
    if len(springs) < sum(counts) + len(counts) - 1:
        return 0

    key = tuple(["".join(springs), *counts])
    if result := cache.get(key):
        return result

    result = 0
    size = counts[0]
    match springs[0]:
        case ".":
            result = arrangements(springs[1:], counts)
        case "#":
            if match_block(springs, size):
                result = arrangements(springs[size + 1 :], counts[1:])
        case _:
            if match_block(springs, size):
                result += arrangements(springs[size + 1 :], counts[1:])
            result += arrangements(springs[1:], counts)

    cache[key] = result
    return result


def part1(input):
    return sum(arrangements(*line) for line in input)


def unfold(springs, counts):
    return list("?".join(["".join(springs)] * 5)), counts * 5


def part2(input):
    return sum(arrangements(*unfold(*line)) for line in input)


def main():
    with open("../input/day_12.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 21


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 525152
