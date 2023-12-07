from itertools import groupby
from functools import cmp_to_key


def parse_input(input):
    return [line.split(" ") for line in input.strip().splitlines()]


def groups(hand):
    return [l for _, g in groupby(sorted(hand)) if (l := len(list(g))) != 1]


def hand_score(hand):
    match groups(hand):
        case [5]:
            return 6
        case [4]:
            return 5
        case [2, 3] | [3, 2]:
            return 4
        case [3]:
            return 3
        case [2, 2]:
            return 2
        case [2]:
            return 1
        case _:
            return 0


def card_score(card):
    return "23456789TJQKA".index(card)


def compare_high_card(a, b) -> int:
    for ca, cb in zip(a, b):
        if (i := card_score(ca)) != (j := card_score(cb)):
            return i - j
    return 0


def compare_hands(a, b) -> int:
    if (i := hand_score(a)) != (j := hand_score(b)):
        return i - j
    else:
        return compare_high_card(a, b)


def compare_hand_bid(a, b) -> int:
    return compare_hands(a[0], b[0])


def score(input, cmp):
    return sum(
        rank * int(bid)
        for rank, (_, bid) in enumerate(sorted(input, key=cmp_to_key(cmp)), 1)
    )


def part1(input):
    return score(input, compare_hand_bid)


# ------------------------------------------------------------------------------


def hand_score_part2(hand):
    jokers = hand.count("J")
    match (groups(c for c in hand if c != "J"), jokers):
        case [5], _:
            return 6
        case [4], _:
            return 5 + jokers
        case ([2, 3] | [3, 2]), _:
            return 4
        case [3], 0:
            return 3
        case [3], 1:
            return 5  # four of a kind
        case [3], 2:
            return 6  # five of a kind
        case [2, 2], 0:
            return 2
        case [2, 2], 1:
            return 4  # full house
        case [2], 0:
            return 1
        case [2], 1:
            return 3  # three of a kind
        case [2], 2:
            return 5  # four of a kind
        case [2], 3:
            return 6  # five of a kind
        case _, 0:
            return 0
        case _, 1:
            return 1  # pair
        case _, 2:
            return 3  # three of a kind
        case _, 3:
            return 5  # four of a kind
        case _, _:
            return 6  # five of a kind


def card_score_part2(card):
    return "J23456789TQKA".index(card)


def compare_high_card_part2(a, b) -> int:
    for ca, cb in zip(a, b):
        if (i := card_score_part2(ca)) != (j := card_score_part2(cb)):
            return i - j
    return 0


def compare_hands_part2(a, b) -> int:
    if (i := hand_score_part2(a)) != (j := hand_score_part2(b)):
        return i - j
    else:
        return compare_high_card_part2(a, b)


def compare_hand_bid_part2(a, b) -> int:
    return compare_hands_part2(a[0], b[0])


def part2(input):
    return score(input, compare_hand_bid_part2)


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 6440


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 5905
