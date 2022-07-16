# --- Part Two ---
#
# To be safe, the CPU also needs to know the highest value held in any register during this process so that it can
# decide how much memory to allocate to these operations. For example, in the above instructions, the highest value
# ever held was 10 (in register c after the third instruction was evaluated).
#


import re
from collections import namedtuple, defaultdict

Instruction = namedtuple("Instruction", "dst_reg inc if_reg cond cond_value")


compare_conds = {
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
}


def step(instr, register_file):
    lhs = register_file[instr.if_reg]
    compare_fn = compare_conds[instr.cond]
    if compare_fn(lhs, instr.cond_value):
        register_file[instr.dst_reg] += instr.inc


def run(instructions):
    highest = None
    register_file = defaultdict(int)
    for instr in instructions:
        step(instr, register_file)
        current = max(register_file.values())
        if highest is None or current > highest:
            highest = current
    return highest


def parse_instr(line):
    m = re.match("^(\w+) (inc|dec) (-?\d+) if (\w+) (<|>|==|!=|<=|>=) (-?\d+)$", line)
    return Instruction(
        dst_reg=m.group(1),
        inc=int(m.group(3)) * (-1 if m.group(2) == "dec" else 1),
        if_reg=m.group(4),
        cond=m.group(5),
        cond_value=int(m.group(6)),
    )


def main():
    with open("../input/day8_1.input.txt") as f:
        highest = run([parse_instr(line) for line in f.readlines()])
        print(highest)


if __name__ == "__main__":
    main()
