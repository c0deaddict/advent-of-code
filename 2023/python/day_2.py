import re


def parse_input(input):
    return [
        [(int(m[1]), m[2]) for m in re.finditer(r"(\d+) (red|green|blue)", line)]
        for line in input.strip().splitlines()
    ]


def part1(input):
    return sum(
        i + 1
        for i, game in enumerate(input)
        if all(n <= 12 for n, color in game if color == "red")
        and all(n <= 13 for n, color in game if color == "green")
        and all(n <= 14 for n, color in game if color == "blue")
    )


def part2(input):
    return sum(
        max(n for n, color in game if color == "red")
        * max(n for n, color in game if color == "green")
        * max(n for n, color in game if color == "blue")
        for game in input
    )


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 8


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 2286
