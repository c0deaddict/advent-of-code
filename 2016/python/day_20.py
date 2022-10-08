def parse_input(input):
    return [tuple(map(int, line.split("-", 2))) for line in input.strip().splitlines()]


def part1(input):
    low = 0
    for (start, end) in sorted(input):
        if low < start:
            return low
        low = max(low, end + 1)


def part2(input):
    low = 0
    allowed = 0
    for (start, end) in sorted(input):
        if low < start:
            allowed += start - low
        low = max(low, end + 1)
    allowed += 2**32 - low
    return allowed


def main():
    with open("../input/day_20.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()
