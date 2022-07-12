from collections import namedtuple

Instruction = namedtuple('Instruction', 'op args')


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
    if instr.op == 'set':
        reg = instr.args[0]
        arg = load(register_file, instr.args[1])
        register_file[reg] = arg
        #print(pc, reg, '=', arg)
    elif instr.op == 'sub':
        reg = instr.args[0]
        arg = load(register_file, instr.args[1])
        register_file[reg] -= arg
        #print(pc, reg, '-', arg, '=', register_file[reg])
    elif instr.op == 'mul':
        reg = instr.args[0]
        arg = load(register_file, instr.args[1])
        register_file[reg] *= arg
        #print(pc, reg, '*', arg, '=', register_file[reg])
    elif instr.op == 'jnz':
        x = load(register_file, instr.args[0])
        if x != 0:
            if instr.args[0] == 'a':
                print('resetting a')
                # register_file['a'] = 0
            offset = load(register_file, instr.args[1])
            #print(pc, 'jnz ', offset, '->', pc+offset)
            pc += offset - 1
        else:
            #print(pc, 'jnz no')
            pass

    return pc + 1


def run(program):
    register_file = dict({chr(ord('a') + i): 0 for i in range(0, 8)})
    register_file['a'] = 1

    pc = 0
    i = 0
    while 0 <= pc < len(program):
        pc = step(program, pc, register_file)
        if register_file['h'] != 0:
            print(register_file['h'])
        elif register_file['g'] == 0:
            print('g=0')
        i += 1
        if i % 500000 == 0:
            print(i, register_file['b'])
        # if i >= 1000:
        #     return

    print(register_file['h'])


def run_optimized():
    b = 107900
    h = 0

    while True:
        f = 1
        for d in range(2, b):
            if b % d == 0:
                f = 0

        if f == 0:
            h = h + 1

        if b == 124900:
            return h

        b = b + 17


def main():
    with open('day23.input.txt') as f:
        # program = [parse_instr(line.strip()) for line in f.readlines()]
        # run(program)
        print(run_optimized())


if __name__ == '__main__':
    main()
