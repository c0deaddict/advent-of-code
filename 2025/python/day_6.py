import operator
from functools import reduce


def parse_input(input):
    return input.splitlines()


def lookup_operator(s):
    return operator.add if s == "+" else operator.mul


def part1(input):
    numbers = [[int(d) for d in line.split()] for line in input[0:-1]]
    operators = input[-1].split()

    return sum(
        reduce(lookup_operator(operators[i]), (row[i] for row in numbers))
        for i in range(len(operators))
    )


def part2(input):
    operators = input[-1]
    rows = len(input) - 1

    result = 0
    i = len(operators) - 1
    numbers = []
    while i >= 0:
        column = "".join(input[j][i] for j in range(rows)).strip()
        if column != "":
            numbers.append(int(column))
        if (op := operators[i]) != " ":
            result += reduce(lookup_operator(op), numbers)
            numbers = []
        i -= 1

    return result


def main():
    with open("../input/day_6.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1.lstrip())) == 4277556


def test_part2():
    assert part2(parse_input(EXAMPLE_1.lstrip())) == 3263827
