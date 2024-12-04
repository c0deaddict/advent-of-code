def parse_input(input):
    return input.strip().splitlines()


def slices(input):
    width = len(input[0])
    height = len(input)
    assert width == height

    for line in input:
        # horizontal
        yield line

    for x in range(width):
        # vertical
        yield [input[y][x] for y in range(height)]

    for i in range(width):
        # diagonal top-left down-right
        yield [input[i + j][j] for j in range(width - i)]
        # diagonal top-right down-left
        yield [input[width - 1 - i - j][j] for j in range(width - i)]

    for i in range(1, height):
        # diagonal top-left down-right
        yield [input[j][i + j] for j in range(height - i)]
        # diagonal top-right down-left
        yield [input[width - 1 - j][i + j] for j in range(height - i)]


def count_xmas(s):
    return "".join(s).count("XMAS") + "".join(reversed(s)).count("XMAS")


def part1(input):
    return sum(count_xmas(s) for s in slices(input))


def is_x_mas_at(input, x, y):
    a = input[y - 1][x - 1] + input[y][x] + input[y + 1][x + 1]
    b = input[y - 1][x + 1] + input[y][x] + input[y + 1][x - 1]
    return (a == "MAS" or a == "SAM") and (b == "MAS" or b == "SAM")


def part2(input):
    height = len(input)
    width = len(input[0])
    return sum(
        int(is_x_mas_at(input, x, y))
        for x in range(1, width - 1)
        for y in range(1, height - 1)
    )


def main():
    with open("../input/day_4.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 18


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 9
