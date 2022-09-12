def parse_input(input):
    return input.strip()


def decompress(input, recurse=False):
    i = 0
    result = 0
    while i < len(input):
        if input[i] == "(":
            marker = ""
            i += 1
            while input[i] != ")":
                marker += input[i]
                i += 1
            i += 1
            l, count = list(map(int, marker.split("x")))
            if recurse:
                result += decompress(input[i : i + l], True) * count
            else:
                result += l * count
            i += l
        else:
            result += 1
            i += 1
    return result


def part1(input):
    return decompress(input)


def part2(input):
    return decompress(input, True)


def main():
    with open("../input/day_9.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1_example1():
    assert part1("ADVENT") == 6


def test_part1_example2():
    assert part1("A(1x5)BC") == 7


def test_part1_example3():
    assert part1("(3x3)XYZ") == 9


def test_part1_example4():
    assert part1("A(2x2)BCD(2x2)EFG") == 11


def test_part1_exmaple5():
    assert part1("(6x1)(1x3)A") == 6


def test_part1_example6():
    assert part1("X(8x2)(3x3)ABCY") == 18


def test_part2_example1():
    assert part2("(3x3)XYZ") == 9


def test_part2_example2():
    assert part2("X(8x2)(3x3)ABCY") == 20


def test_part2_example3():
    assert part2("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920


def test_part2_example4():
    assert part2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445
