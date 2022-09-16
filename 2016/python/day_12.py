def parse_input(input):
    return [line.split() for line in input.strip().splitlines()]


def reg_or_const(val, regs):
    try:
        return int(val)
    except:
        return regs[val]


def run(prog, regs):
    ip = 0
    while True:
        try:
            instr = prog[ip]
        except:
            break
        ip += 1
        if instr[0] == "cpy":
            regs[instr[2]] = reg_or_const(instr[1], regs)
        elif instr[0] == "inc":
            regs[instr[1]] += 1
        elif instr[0] == "dec":
            regs[instr[1]] -= 1
        elif instr[0] == "jnz":
            if reg_or_const(instr[1], regs) != 0:
                ip += int(instr[2]) - 1


def part1(prog):
    regs = dict(a=0, b=0, c=0, d=0)
    run(prog, regs)
    return regs["a"]


def part2(prog):
    regs = dict(a=0, b=0, c=1, d=0)
    run(prog, regs)
    return regs["a"]


def main():
    with open("../input/day_12.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 42
