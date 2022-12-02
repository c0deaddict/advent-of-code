def parse_input(input):
    return [line.split() for line in input.strip().splitlines()]


def score(game):
    opponent = dict(A=0, B=1, C=2)[game[0]]
    me = dict(X=0, Y=1, Z=2)[game[1]]
    if me == opponent:
        return 3 + me + 1
    elif (me - 1) % 3 == opponent:
        return 6 + me + 1
    else:
        return me + 1


def part1(input):
    return sum(map(score, input))


def score_part2(game):
    opponent = dict(A=0, B=1, C=2)[game[0]]
    if game[1] == "X":
        return 0 + (opponent - 1) % 3 + 1
    elif game[1] == "Y":
        return 3 + opponent + 1
    elif game[1] == "Z":
        return 6 + (opponent + 1) % 3 + 1


def part2(input):
    return sum(map(score_part2, input))


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
A Y
B X
C Z
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 15


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 12
