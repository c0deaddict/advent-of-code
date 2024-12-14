import re
import dataclasses
from dataclasses import dataclass

from lib import Vector


@dataclass
class Machine:
    a: Vector
    b: Vector
    price: Vector


def parse_machine(block):
    return Machine(
        *[Vector(*map(int, re.findall(r"\d+", line))) for line in block.splitlines()]
    )


def parse_input(input):
    return [parse_machine(block) for block in input.strip().split("\n\n")]


def solve_machine(m: Machine) -> int:
    #
    # p(rice) = a * i + b * j
    #
    # p.x = a.x * i + b.x * j
    # p.y = a.y * i + b.y * j
    #
    # i = (p.x - b.x * j) / a.x
    # j = (p.y - a.y * i) / b.y
    #
    # substitute j in "i equation", and rewrite leads to:
    # i = (b.x * p.y - p.x * b.y) / (b.x * a.y - a.x * b.y)
    #
    num = m.b.x * m.price.y - m.price.x * m.b.y
    denom = m.b.x * m.a.y - m.a.x * m.b.y
    i, remainder = divmod(num, denom)
    if remainder != 0:
        return 0  # no integer solution
    j, remainder = divmod(m.price.x - (i * m.a.x), m.b.x)
    if remainder != 0:
        return 0
    return i * 3 + j


def part1(input):
    return sum(solve_machine(m) for m in input)


def extend_input(input):
    inc = 10000000000000
    offset = Vector(x=inc, y=inc)
    return [dataclasses.replace(m, price=m.price + offset) for m in input]


def part2(input):
    return sum(solve_machine(m) for m in extend_input(input))


def main():
    with open("../input/day_13.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 480


def test_part2():
    input = extend_input(parse_input(EXAMPLE_1))
    assert [solve_machine(m) > 0 for m in input] == [False, True, False, True]
