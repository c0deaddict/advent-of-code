# --- Part Two ---
#
# Now, the jumps are even stranger: after each jump, if the offset was three or more, instead decrease it by 1.
# Otherwise, increase it by 1 as before.
#
# Using this rule with the above example, the process now takes 10 steps, and the offset values after finding the
# exit are left as 2 3 2 3 -1.
#
# How many steps does it now take to reach the exit?


def step(program, pc):
    offset = program[pc]
    if offset >= 3:
        program[pc] -= 1
    else:
        program[pc] += 1
    return pc + offset


def run(program):
    pc = 0
    steps = 0
    try:
        while True:
            pc = step(program, pc)
            steps += 1
    except IndexError:
        return steps


def main():
    with open("../input/day5_1.input.txt") as f:
        program = [int(line.strip()) for line in f.readlines()]

    print(run(program))


if __name__ == "__main__":
    main()
