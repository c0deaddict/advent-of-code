def parse_input(input):
    return [
        tuple(int(id.strip()) for id in pair.split("-"))
        for pair in input.strip().split(",")
    ]


def is_invalid(id):
    s = str(id)
    l = len(s)
    return l % 2 == 0 and s[: l // 2] == s[l // 2 :]


def part1(input):
    return sum(
        id
        for start, stop in input
        for id in range(start, stop+1)
        if is_invalid(id)
    )


def is_invalid_part2(id):
    s = str(id)
    l = len(s)
    for i in range(1, 1 + l // 2):
        if l % i == 0 and s[0:i] * (l // i) == s:
            return True
    return False


def part2(input):
    return sum(
        id
        for start, stop in input
        for id in range(start, stop+1)
        if is_invalid_part2(id)
    )


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 1227775554


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 4174379265
