from collections import namedtuple

Instruction = namedtuple("Instruction", "op args")


def parse_arg(arg):
    try:
        return int(arg)
    except ValueError:
        return arg


def parse_instr(line):
    op, *args = line.split()
    return Instruction(op=op, args=[parse_arg(arg) for arg in args])


def load(register_file, arg):
    if type(arg) is int:
        return arg
    else:
        return register_file[arg]


def step(program, pc, register_file):
    instr = program[pc]
    if instr.op == "set":
        arg = load(register_file, instr.args[1])
        register_file[instr.args[0]] = arg
    elif instr.op == "sub":
        arg = load(register_file, instr.args[1])
        register_file[instr.args[0]] -= arg
    elif instr.op == "mul":
        arg = load(register_file, instr.args[1])
        register_file[instr.args[0]] *= arg
    elif instr.op == "jnz":
        x = load(register_file, instr.args[0])
        if x != 0:
            offset = load(register_file, instr.args[1])
            pc += offset - 1

    return pc + 1, instr.op


def run(program):
    executed_mul = 0
    register_file = dict({chr(ord("a") + i): 0 for i in range(0, 8)})
    pc = 0
    while 0 <= pc < len(program):
        pc, op = step(program, pc, register_file)
        if op == "mul":
            executed_mul += 1
    return executed_mul


def main():
    with open("../input/day23.input.txt") as f:
        program = [parse_instr(line.strip()) for line in f.readlines()]
        print(run(program))


if __name__ == "__main__":
    main()
