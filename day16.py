# --- Day 16: Permutation Promenade ---
#
# You come upon a very unusual sight; a group of programs here appear to be dancing.
#
# There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b
# stands in position 1, and so on until p, which stands in position 15.
#
# The programs' dance consists of a sequence of dance moves:
#
#     Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise.
# (For example, s3 on abcde produces cdeab).
#     Exchange, written xA/B, makes the programs at positions A and B swap places.
#     Partner, written pA/B, makes the programs named A and B swap places.
#
# For example, with only five programs standing in a line (abcde), they could do the following dance:
#
#     s1, a spin of size 1: eabcd.
#     x3/4, swapping the last two programs: eabdc.
#     pe/b, swapping programs e and b: baedc.
#
# After finishing their dance, the programs end up in order baedc.
#
# You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs
# standing after their dance?
#
# --- Part Two ---
#
# Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.
#
# Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including
# the first dance, a total of one billion (1000000000) times.
#
# In the example above, their second dance would begin with the order baedc, and use the same dance moves:
#
#     s1, a spin of size 1: cbaed.
#     x3/4, swapping the last two programs: cbade.
#     pe/b, swapping programs e and b: ceadb.
#
# In what order are the programs standing after their billion dances?


import time

STEP = 's'
EXCHANGE = 'x'
PARTNER = 'p'


def init():
    return [chr(i + ord('a')) for i in range(0, 16)]


def swap(programs, i, j):
    tmp = programs[i]
    programs[i] = programs[j]
    programs[j] = tmp


def step(programs, move):
    if move[0] == STEP:
        num = move[1]
        idx = len(programs) - num
        section = programs[idx:]
        del programs[idx:]
        for p in reversed(section):
            programs.insert(0, p)

    elif move[0] == EXCHANGE:
        swap(programs, move[1], move[2])
    elif move[0] == PARTNER:
        i = programs.index(move[1])
        j = programs.index(move[2])
        swap(programs, i, j)


def parse_move(str):
    t = str[0]
    if t == STEP:
        return STEP, int(str[1:])
    elif t == 'x':
        a, b = str[1:].split('/', 1)
        return EXCHANGE, int(a), int(b)
    elif t == 'p':
        a, b = str[1:].split('/', 1)
        return PARTNER, a, b


def dance(programs, moves):
    for move in moves:
        step(programs, move)


def main():
    with open('day16.input.txt') as f:
        moves = [parse_move(str) for str in f.read().split(',')]

    programs = init()
    for i in range(0, 1000):
        dance(programs, moves)

    print(''.join(programs))


if __name__ == '__main__':
    t = time.time()
    main()
    print(time.time() - t)
