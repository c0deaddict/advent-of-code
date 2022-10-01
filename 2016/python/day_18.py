def parse_input(input):
    return input.strip()


def is_trap(c):
    return c == "^"


def deduce_tile(prev, i):
    left = is_trap(prev[i - 1]) if i > 0 else False
    center = is_trap(prev[i])
    right = is_trap(prev[i + 1]) if i < len(prev) - 1 else False

    trap = (
        # left and center tiles are traps, but its right tile is not
        (left and center and not right)
        or
        # center and right tiles are traps, but its left tile is not
        (center and right and not left)
        or
        # only its left tile is a trap
        (left and not center and not right)
        or
        # only its right tile is a trap
        (right and not center and not left)
    )

    return "^" if trap else "."


def next_row(prev):
    return "".join(deduce_tile(prev, i) for i, _ in enumerate(prev))


def make_rows(input, num):
    prev = input
    for _ in range(num):
        yield prev
        prev = next_row(prev)


def count_safe(rows):
    return sum(row.count(".") for row in rows)


def part1(input):
    return count_safe(make_rows(input, 40))


def part2(input):
    return count_safe(make_rows(input, 400000))


def main():
    with open("../input/day_18.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert count_safe(make_rows(".^^.^.^^^^", 10)) == 38
