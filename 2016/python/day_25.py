from itertools import islice, count


def parse_input(input):
    return [line.split() for line in input.strip().splitlines()]


def reg_or_const(val, regs):
    return regs[val] if val in regs else int(val)


def run(prog, regs):
    ip = 0
    while 0 <= ip < len(prog):
        instr = prog[ip]
        ip += 1
        if instr[0] == "cpy":
            if instr[2] in regs:
                regs[instr[2]] = reg_or_const(instr[1], regs)
        elif instr[0] == "inc":
            regs[instr[1]] += 1
        elif instr[0] == "dec":
            regs[instr[1]] -= 1
        elif instr[0] == "jnz":
            if reg_or_const(instr[1], regs) != 0:
                ip += reg_or_const(instr[2], regs) - 1
        elif instr[0] == "out":
            yield reg_or_const(instr[1], regs)
        else:
            raise Exception(f"unknown instruction: {instr[0]}")


def part1(input):
    for i in count(start=1):
        regs = dict(a=i, b=0, c=0, d=0)
        if list(islice(run(input, regs), 8)) == [0, 1, 0, 1] * 2:
            return i


def part2(input):
    pass


def main():
    with open("../input/day_25.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()
