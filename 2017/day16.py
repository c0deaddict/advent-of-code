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

STEP = 's'
EXCHANGE = 'x'
PARTNER = 'p'

COUNT = 16


def init():
    return [chr(i + ord('a')) for i in range(0, COUNT)]


def interpret_move(spin, programs, move):
    if move[0] == STEP:
        return (spin + move[1]) % COUNT
    elif move[0] == EXCHANGE:
        i = (move[1] - spin) % COUNT
        j = (move[2] - spin) % COUNT
        tmp = programs[i]
        programs[i] = programs[j]
        programs[j] = tmp
        return spin
    elif move[0] == PARTNER:
        i = programs.index(move[1])
        j = programs.index(move[2])
        programs[i] = move[2]
        programs[j] = move[1]
        return spin


def compile_move(move):
    if move[0] == STEP:
        params = dict(spin=move[1], count=COUNT)
        yield '# s{spin}'.format(**params)
        yield 'spin = (spin + {spin}) % {count}'.format(**params)
    elif move[0] == EXCHANGE:
        params = dict(i=move[1], j=move[2], count=COUNT)
        yield '# e{i}/{j}'.format(**params)
        yield 'i = ({i} - spin) % {count}'.format(**params)
        yield 'j = ({j} - spin) % {count}'.format(**params)
        yield 'tmp = programs[i]'
        yield 'programs[i] = programs[j]'
        yield 'programs[j] = tmp'
    elif move[0] == PARTNER:
        params = dict(a=move[1], b=move[2])
        yield '# p{a}/{b}'.format(**params)
        yield "i = programs.index('{a}')".format(**params)
        yield "j = programs.index('{b}')".format(**params)
        yield "programs[i] = '{b}'".format(**params)
        yield "programs[j] = '{a}'".format(**params)


def compile_program(moves):
    yield 'def compiled_dance(spin, programs):'
    for move in moves:
        yield from ['    ' + line for line in compile_move(move)]
    yield '    return spin'
    yield ''


def compile_move_c(move):
    if move[0] == STEP:
        return '''// s{spin}
spin = (spin + {spin}) % {count};
'''.format(spin=move[1], count=COUNT)
    elif move[0] == EXCHANGE:
        return '''//# e{i}/{j}
i = mod(({i} - spin), {count});
j = mod(({j} - spin), {count});
tmp = programs[i];
programs[i] = programs[j];
programs[j] = tmp;
'''.format(i=move[1], j=move[2], count=COUNT)
    elif move[0] == PARTNER:
        return '''// p{a}/{b}
for (int k = 0; k < {count}; k++) {{
    if (programs[k] == '{a}') i = k;
    if (programs[k] == '{b}') j = k;
}}
programs[i] = '{b}';
programs[j] = '{a}';
'''.format(a=move[1], b=move[2], count=COUNT)


def compile_program_c(moves):
    yield 'static inline int mod(int a, int b) {'
    yield 'int ret = a % b;'
    yield 'if (ret < 0) ret += b;'
    yield 'return ret;'
    yield '}'
    yield ''
    yield 'int compiled_dance(int spin, char *programs) {'
    yield 'char tmp;'
    yield 'int i, j;'
    for move in moves:
        yield compile_move_c(move)
    yield 'return spin;'
    yield '}'


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


def dance(spin, programs, moves):
    for move in moves:
        spin = interpret_move(spin, programs, move)
    return spin


def final_spin(spin, programs):
    return programs[-spin:] + programs[:-spin]


def main():
    with open('day16.input.txt') as f:
        moves = [parse_move(str) for str in f.read().split(',')]

    program = '\n'.join(compile_program(moves))

    with open('day16_dance.c', 'w') as f:
        c_program = '\n'.join(compile_program_c(moves))
        f.write(c_program)

    exports = dict()
    exec(program, exports)
    compiled_dance = exports['compiled_dance']

    # Find the cycle time.
    history = list()
    cycles = 0
    spin = 0
    programs = init()
    while True:
        spin = compiled_dance(spin, programs)
        current = ''.join(final_spin(spin, programs))
        if current in history:
            break
        history.append(current)
        cycles += 1

    cycle_time = cycles - history.index(current)
    rem = (1000000000 - (cycles + 1)) % cycle_time
    for i in range(0, rem):
        spin = compiled_dance(spin, programs)

    print(''.join(final_spin(spin, programs)))


if __name__ == '__main__':
    main()
