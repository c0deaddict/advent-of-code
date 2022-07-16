# --- Day 8: I Heard You Like Registers ---
#
# You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like
# you to compute the result of a series of unusual register instructions.
#
# Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's
# value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction
# without modifying the register. The registers all start at 0. The instructions look like this:
#
# b inc 5 if a > 1
# a inc 1 if b < 5
# c dec -10 if a >= 1
# c inc -20 if c == 10
#
# These instructions would be processed as follows:
#
#     Because a starts at 0, it is not greater than 1, and so b is not modified.
#     a is increased by 1 (to 1) because b is less than 5 (it is 0).
#     c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
#     c is increased by -20 (to -10) because c is equal to 10.
#
# After this process, the largest value in any register is 1.
#
# You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth
# to tell you what all the registers are named, and leaves that to you to determine.
#
# What is the largest value in any register after completing the instructions in your puzzle input?

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
    register_file = defaultdict(int)
    for instr in instructions:
        step(instr, register_file)
    return register_file


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
        register_file = run([parse_instr(line) for line in f.readlines()])
        print(max(register_file.values()))


if __name__ == "__main__":
    main()
