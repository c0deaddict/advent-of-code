import random
from statistics import median
import pytest

def parse_input(input):
    return list(map(int, input.strip().split(",")))

def compute_fuel(input, pos):
    return sum(abs(x - pos) for x in input)

def part1(input):
    return compute_fuel(input, int(median(input)))

# 1 + 2 + ... + i
def triangle_number(n):
    return (n * (n + 1)) // 2

def compute_fuel_part2(input, pos):
    return sum(triangle_number(abs(x - pos)) for x in input)

def part2(input):
    return min(
        compute_fuel_part2(input, i)
        for i in range(min(input), max(input)+1)
    )

def main():
    with open("../input/day_07.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))

if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = "16,1,2,0,4,2,7,1,2,14"

def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 37

def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_1)) == 168

def test_median_works():
    for i in range(0, 1000):
        input = [random.randint(0, 50) for _ in range(0, 100)]
        assert part1(input) == min(compute_fuel(input, i) for i in input)
