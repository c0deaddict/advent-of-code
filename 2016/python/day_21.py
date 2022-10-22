import re
from functools import partial


def swap(x, y, pw):
    res = pw[:]
    res[x] = pw[y]
    res[y] = pw[x]
    return res


def swap_letters(x, y, pw):
    return [y if c == x else x if c == y else c for c in pw]


def rotate_left(x, pw):
    i = x % len(pw)
    return pw[i:] + pw[0:i]


def rotate_right(x, pw):
    i = x % len(pw)
    return pw[-i:] + pw[0:-i]


def rotate_position(x, pw):
    i = pw.index(x)
    if i >= 4:
        i += 1
    return rotate_right(i + 1, pw)


def inverse_rotate_position(x, pw):
    result = pw
    for i in range(len(pw)):
        result = rotate_left(1, result)
        if rotate_position(x, result) == pw:
            return result


def reverse(x, y, pw):
    return pw[0:x] + list(reversed(pw[x : y + 1])) + pw[y + 1 :]


def move(x, y, pw):
    res = pw[0:x] + pw[x + 1 :]
    return res[0:y] + pw[x : x + 1] + res[y:]


def parse_instr(line):
    if m := re.match(r"^swap position (\d+) with position (\d+)$", line):
        fn = partial(swap, int(m.group(1)), int(m.group(2)))
        return fn, fn
    elif m := re.match(r"^swap letter ([a-z]) with letter ([a-z])$", line):
        fn = partial(swap_letters, m.group(1), m.group(2))
        return fn, fn
    elif m := re.match(r"^rotate (left|right) (\d+) steps?$", line):
        fn, inv = (
            (rotate_left, rotate_right)
            if m.group(1) == "left"
            else (rotate_right, rotate_left)
        )
        steps = int(m.group(2))
        return partial(fn, steps), partial(inv, steps)
    elif m := re.match(r"^rotate based on position of letter ([a-z])$", line):
        fn = partial(rotate_position, m.group(1))
        inv = partial(inverse_rotate_position, m.group(1))
        return fn, inv
    elif m := re.match(r"^reverse positions (\d+) through (\d+)$", line):
        fn = partial(reverse, int(m.group(1)), int(m.group(2)))
        return fn, fn
    elif m := re.match(r"^move position (\d+) to position (\d+)$", line):
        i, j = int(m.group(1)), int(m.group(2))
        return partial(move, i, j), partial(move, j, i)
    else:
        raise line


def parse_input(input):
    return [parse_instr(line) for line in input.strip().splitlines()]


def scramble(input, password):
    result = list(password)
    for fn, _ in input:
        result = fn(result)
    return "".join(result)


def unscramble(input, password):
    result = list(password)
    for _, fn in reversed(input):
        result = fn(result)
    return "".join(result)


def part1(input):
    return scramble(input, "abcdefgh")


def part2(input):
    return unscramble(input, "fbgdceah")


def main():
    with open("../input/day_21.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""


def test_part1():
    assert rotate_left(2, list("abcd")) == list("cdab")
    assert rotate_right(1, list("abcd")) == list("dabc")
    assert reverse(1, 2, list("abcd")) == list("acbd")
    assert move(1, 4, list("bcdea")) == list("bdeac")
    assert move(3, 0, list("bdeac")) == list("abdec")
    assert scramble(parse_input(EXAMPLE_1), "abcde") == "decab"


def test_inverse_rotate():
    assert inverse_rotate_position("b", list("ecabd")) == list("abdec")
    assert inverse_rotate_position("d", list("decab")) == list("ecabd")


def test_part2():
    input = parse_input(EXAMPLE_1)
    assert unscramble(input, scramble(input, "abcde")) == "abcde"
