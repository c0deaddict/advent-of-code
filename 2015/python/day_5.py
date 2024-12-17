import re


def parse_input(input):
    return input.strip().splitlines()


def is_nice(s):
    return (
        len(re.findall(r"[aeiou]", s)) >= 3
        and bool(re.search(r"([a-z])\1", s))
        and not bool(re.search(r"ab|cd|pq|xy", s))
    )


def part1(input):
    return sum(int(is_nice(s)) for s in input)


def part2(input):
    pass


def main():
    with open("../input/day_5.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")
