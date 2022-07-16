def parse_grid(str):
    return str.split("/")


def parse_rule(line):
    left, right = line.strip().split(" => ")
    return parse_grid(left), parse_grid(right)


def unit(grid):
    return grid


def flip_horz(grid):
    return list(reversed(grid))


def flip_vert(grid):
    return [row[::-1] for row in grid]


def rotate_90(grid):
    res = [""] * len(grid[0])
    for row in reversed(grid):
        for i, c in enumerate(row):
            res[i] += c
    return res


def rotate_180(grid):
    return flip_horz(flip_vert(grid))


def rotate_270(grid):
    res = [""] * len(grid[0])
    for row in grid:
        for i, c in enumerate(reversed(row)):
            res[i] += c
    return res


def compose(f, g):
    return lambda x: g(f(x))


def convert(rules, grid):
    trans = [
        (unit, unit),
        (flip_horz, flip_horz),
        (flip_vert, flip_vert),
        (rotate_90, rotate_270),
        (rotate_180, rotate_180),
        (rotate_270, rotate_90),
        (compose(rotate_90, flip_vert), compose(flip_vert, rotate_270)),
        (compose(rotate_90, flip_horz), compose(flip_horz, rotate_270)),
    ]

    for rule, replacement in rules:
        for f, g in trans:
            if rule == f(grid):
                return replacement

    raise ValueError("no match found")


def iterate(rules, grid):
    size = 2 if len(grid) % 2 == 0 else 3
    result = []
    for i in range(0, len(grid), size):
        row = []
        for j in range(0, len(grid[i]), size):
            subgrid = [row[j : j + size] for row in grid[i : i + size]]
            row.append(convert(rules, subgrid))

        for cells in zip(*row):
            result.append("".join(cells))

    return result


def run(rules, grid, num):
    for i in range(0, num):
        grid = iterate(rules, grid)
        # print(i)
        # print('\n'.join(grid))
        # print()
    return grid


def main():
    with open("../input/day21.input.txt") as f:
        rules = [parse_rule(line) for line in f.readlines()]

    start = [".#.", "..#", "###"]
    grid = run(rules, start, 5)
    print("".join(grid).count("#"))

    grid = run(rules, start, 18)
    print("".join(grid).count("#"))


if __name__ == "__main__":
    main()
