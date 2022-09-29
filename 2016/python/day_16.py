def parse_input(input):
    return input.strip()


def checksum(stream):
    if len(stream) % 2 == 1:
        return stream

    result = ""
    for i in range(0, len(stream), 2):
        result += "1" if stream[i] == stream[i + 1] else "0"

    return checksum(result)


def flip(bit):
    return "0" if bit == "1" else "1"


def fill_disk(initial, length):
    if len(initial) >= length:
        return initial[:length]

    return fill_disk(initial + "0" + "".join(map(flip, reversed(initial))), length)


def part1(input):
    return checksum(fill_disk(input, 272))


def part2(input):
    return checksum(fill_disk(input, 35651584))


def main():
    with open("../input/day_16.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_checksum():
    assert checksum("110010110100") == "100"


def test_part1():
    assert checksum(fill_disk("10000", 20)) == "01100"
