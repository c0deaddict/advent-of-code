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
    elves = [1] * input
    count = input
    next = {i: (i + 1) % input for i in range(input)}
    across = {i: (i + input // 2) % input for i in range(input)}
    i = 0
    while True:
        # j = i
        # for _ in range(count // 2):
        #     prev = j
        #     j = next[j]
        j = across[i]

        print(f"Elf {i+1} steales Elf {j+1}'s presents")
        elves[i] += elves[j]
        elves[j] = 0

        # next[prev] = next[j]

        count -= 1
        if count == 1:
            return i + 1

        i = next[i]


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
