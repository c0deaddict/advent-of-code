def parse_input(input):
    return input.strip()


def find_marker(input, prefix_len):
    for i in range(prefix_len, len(input)):
        if len(set(input[i - prefix_len : i])) == prefix_len:
            return i


def part1(input):
    return find_marker(input, 4)


def part2(input):
    return find_marker(input, 14)


def main():
    with open("../input/day_6.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1(parse_input("mjqjpqmgbljsphdztnvjfqwrcgsmlb")) == 7
    assert part1(parse_input("bvwbjplbgvbhsrlpgdmjqwftvncz")) == 5
    assert part1(parse_input("nppdvjthqldpwncqszvftbrmjlhg")) == 6
    assert part1(parse_input("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")) == 10
    assert part1(parse_input("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")) == 11


def test_part2():
    assert part2(parse_input("mjqjpqmgbljsphdztnvjfqwrcgsmlb")) == 19
    assert part2(parse_input("bvwbjplbgvbhsrlpgdmjqwftvncz")) == 23
    assert part2(parse_input("nppdvjthqldpwncqszvftbrmjlhg")) == 23
    assert part2(parse_input("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")) == 29
    assert part2(parse_input("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")) == 26
