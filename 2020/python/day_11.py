def parse_input(input):
    return [line.split(" ", 2) for line in input.strip().splitlines()]


def part1(input):
    pc = 0
    acc = 0
    visited = [False for _ in input]
    while not visited[pc]:
        visited[pc] = True
        instr = input[pc]
        pc += 1
        if instr[0] == "acc":
            acc += int(instr[1])
        elif instr[0] == "jmp":
            pc += int(instr[1]) - 1
    return acc


def part2(input):
    pass


def main():
    with open("../input/day_8.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 37
