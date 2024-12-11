from collections import Counter, defaultdict


def parse_input(input):
    return [int(i) for i in input.strip().split()]


def iteration(stones):
    result = defaultdict(lambda: 0)
    for i, count in stones.items():
        if i == 0:
            result[1] += count
        elif (l := len(s := str(i))) % 2 == 0:
            result[int(s[0 : l // 2])] += count
            result[int(s[l // 2 :])] += count
        else:
            result[i * 2024] += count
    return result


def part1(input, n=25):
    stones = Counter(input)
    for _ in range(n):
        stones = iteration(stones)
    return sum(stones.values())


def part2(input):
    return part1(input, 75)


def main():
    with open("../input/day_11.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_iteration():
    input = parse_input("0 1 10 99 999")
    assert iteration(Counter(input)) == Counter([1, 2024, 1, 0, 9, 9, 2021976])


def test_part1():
    assert part1(parse_input("125 17"), 6) == 22
    assert part1(parse_input("125 17"), 25) == 55312
