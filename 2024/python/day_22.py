from itertools import islice
from collections import defaultdict


def parse_input(input):
    return [int(line) for line in input.strip().splitlines()]


def next_secret(s):
    s = (s ^ (s * 64)) % 16777216
    s = (s ^ (s // 32)) % 16777216
    s = (s ^ (s * 2048)) % 16777216
    return s


def secret_sequence(s):
    yield s
    while True:
        s = next_secret(s)
        yield s


def part1(input):
    return sum(next(islice(secret_sequence(s), 2000, None)) for s in input)


def prices_sequence(s):
    return (s % 10 for s in secret_sequence(s))


def changes(seq):
    prev = None
    for i in seq:
        if prev is not None:
            yield i - prev
        prev = i


def groups(seq, n):
    window = [next(seq) for _ in range(n - 1)]
    for i, v in enumerate(seq):
        window.append(v)
        yield n + i, tuple(window)
        window.pop(0)


def part2(input):
    choices = defaultdict(lambda: 0)
    for secret in input:
        prices = list(islice(prices_sequence(secret), 2001))
        visited = set()
        for i, seq in groups(changes(prices), 4):
            if seq not in visited:
                choices[seq] += prices[i]
                visited.add(seq)
    return max(choices.values())


def main():
    with open("../input/day_22.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
1
10
100
2024
"""


EXAMPLE_2 = """
1
2
3
2024
"""


def test_next_secret():
    assert list(islice(secret_sequence(123), 1, 11)) == [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 37327623


def test_changes():
    assert list(islice(changes(prices_sequence(123)), 9)) == [
        -3,
        6,
        -1,
        -1,
        0,
        2,
        -2,
        0,
        -2,
    ]


def test_groups():
    assert list(islice(groups(changes(prices_sequence(123)), 4), 6)) == [
        (4, (-3, 6, -1, -1)),
        (5, (6, -1, -1, 0)),
        (6, (-1, -1, 0, 2)),
        (7, (-1, 0, 2, -2)),
        (8, (0, 2, -2, 0)),
        (9, (2, -2, 0, -2)),
    ]


def test_part2():
    assert part2(parse_input(EXAMPLE_2)) == 23
