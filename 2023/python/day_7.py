from itertools import groupby
from functools import cmp_to_key, partial
from enum import IntEnum


def parse_input(input):
    return [line.split(" ") for line in input.strip().splitlines()]


def groups(hand):
    return [l for _, g in groupby(sorted(hand)) if (l := len(list(g))) != 1]


class HandScore(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0

    @classmethod
    def score(cls, hand):
        match groups(hand):
            case [5]:
                return cls.FIVE_OF_A_KIND
            case [4]:
                return cls.FOUR_OF_A_KIND
            case [2, 3] | [3, 2]:
                return cls.FULL_HOUSE
            case [3]:
                return cls.THREE_OF_A_KIND
            case [2, 2]:
                return cls.TWO_PAIR
            case [2]:
                return cls.PAIR
            case _:
                return cls.HIGH_CARD

    def add_joker(self):
        match self:
            case HandScore.FOUR_OF_A_KIND:
                return HandScore.FIVE_OF_A_KIND
            case HandScore.THREE_OF_A_KIND:
                return HandScore.FOUR_OF_A_KIND
            case HandScore.TWO_PAIR:
                return HandScore.FULL_HOUSE
            case HandScore.PAIR:
                return HandScore.THREE_OF_A_KIND
            case HandScore.HIGH_CARD:
                return HandScore.PAIR
            case _:
                return self


def compare_strings(order, a, b) -> int:
    for ca, cb in zip(a, b):
        if (i := order.index(ca)) != (j := order.index(cb)):
            return i - j
    return 0


def compare_hands(hand_score, card_order, a, b) -> int:
    if (i := hand_score(a)) != (j := hand_score(b)):
        return i - j
    else:
        # Compare high card
        return partial(compare_strings, card_order)(a, b)


def compare_hand_bid(hand_score, card_order, a, b) -> int:
    return compare_hands(hand_score, card_order, a[0], b[0])


def score(input, cmp):
    return sum(
        rank * int(bid)
        for rank, (_, bid) in enumerate(sorted(input, key=cmp_to_key(cmp)), 1)
    )


def part1(input):
    return score(input, partial(compare_hand_bid, HandScore.score, "23456789TJQKA"))


def hand_score_part2(hand):
    s = HandScore.score(c for c in hand if c != "J")
    for _ in range(hand.count("J")):
        s = s.add_joker()
    return s


def part2(input):
    return score(input, partial(compare_hand_bid, hand_score_part2, "J23456789TQKA"))


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
