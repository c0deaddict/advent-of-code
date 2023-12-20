def parse_instruction(line):
    op, args = line.split(" ", 1)
    return tuple([op] + [v.strip() for v in args.split(",")])


def parse_input(input):
    return [parse_instruction(line) for line in input.strip().splitlines()]


def run(prog, regs):
    pc = 0
    while 0 <= pc < len(prog):
        match prog[pc]:
            case "hlf", r:
                regs[r] //= 2
            case "tpl", r:
                regs[r] *= 3
            case "inc", r:
                regs[r] += 1
            case "jmp", offset:
                pc += int(offset)
                continue
            case "jie", r, offset if regs[r] % 2 == 0:
                pc += int(offset)
                continue
            case "jio", r, offset if regs[r] == 1:
                pc += int(offset)
                continue
        pc += 1
    return regs


def part1(input):
    return run(input, dict(a=0, b=0))["b"]


def part2(input):
    return run(input, dict(a=1, b=0))["b"]


def main():
    with open("../input/day_23.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
inc a
jio a, +2
tpl a
inc a
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 0
