def parse_input(input):
    return int(input.strip())


def part1(input):
    elves = [1] * input
    next = {i: (i + 1) % input for i in range(input)}
    i = 0
    while True:
        j = next[i]
        if i == j:
            return i + 1

        elves[i] += elves[j]
        elves[j] = 0

        next[i] = next[j]
        i = next[j]


def part2(input):
    for i in range(input):
        if 3**i > input - 1:
            start = 3 ** (i - 1)
            if input <= start * 2:
                return input - start
            else:
                return start + (input - start * 2) * 2


def main():
    with open("../input/day_19.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1(5) == 3


def test_part2():
    assert part2(5) == 2
