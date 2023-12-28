import re


def parse_input(input):
    return [
        re.match(r"^(\d+)-(\d+) ([a-z]): (.+)$", line).groups()
        for line in input.splitlines()
    ]


def validate(min, max, letter, password):
    return int(min) <= password.count(letter) <= int(max)


def part1(input):
    return sum(1 for entry in input if validate(*entry))


def validate_part2(min, max, letter, password):
    a = password[int(min) - 1] == letter
    b = password[int(max) - 1] == letter
    return (a or b) and not (a and b)


def part2(input):
    return sum(1 for entry in input if validate_part2(*entry))


def main():
    with open("../input/day_2.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()
