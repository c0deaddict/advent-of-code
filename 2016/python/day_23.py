from copy import deepcopy


def parse_input(input):
    return [line.split() for line in input.strip().splitlines()]


def print_prog(prog):
    print("\n".join([str(i) + ": " + " ".join(instr) for i, instr in enumerate(prog)]))


def reg_or_const(val, regs):
    return regs[val] if val in regs else int(val)


def toggle(instr):
    if len(instr) == 2:
        return ["dec" if instr[0] == "inc" else "inc", instr[1]]
    else:
        return ["cpy" if instr[0] == "jnz" else "jnz", instr[1], instr[2]]


def run(prog, regs):
    prog = deepcopy(prog)
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
        elif instr[0] == "tgl":
            tgt = ip - 1 + int(reg_or_const(instr[1], regs))
            if 0 <= tgt < len(prog):
                print_prog(prog)
                prog[tgt] = toggle(prog[tgt])
        elif instr[0] == "mul":
            regs[instr[2]] *= reg_or_const(instr[1], regs)
        elif instr[0] == "add":
            regs[instr[2]] += reg_or_const(instr[1], regs)
        elif instr[0] == "nop":
            pass
        else:
            raise Exception(f"unknown instruction: {instr[0]}")


def part1(input):
    regs = dict(a=7, b=0, c=0, d=0)
    run(input, regs)
    return regs["a"]


def part2(input):
    prog = deepcopy(input)
    prog[5] = ["mul", "d", "c"]
    prog[6] = ["add", "c", "a"]
    prog[7:10] = [["nop"]] * 3
    print_prog(prog)
    regs = dict(a=12, b=0, c=0, d=0)
    run(prog, regs)
    return regs["a"]


def main():
    with open("../input/day_23.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 3
