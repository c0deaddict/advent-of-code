def parse_input(input):
    return input.strip().split(", ")


def travel(input):
    dir = 0
    x, y = 0, 0
    yield (x, y)
    for i in input:
        forward = int(i[1:])
        dir = (dir + (1 if i[0] == "R" else -1)) % 4
        for _ in range(forward):
            if dir == 0:
                y -= 1
            elif dir == 1:
                x += 1
            elif dir == 2:
                y += 1
            else:
                x -= 1
            yield (x, y)


def manhattan(x, y):
    return abs(x) + abs(y)


def part1(input):
    *_, p = travel(input)
    return manhattan(*p)


def part2(input):
    visited = set()
    for p in travel(input):
        if p in visited:
            return manhattan(*p)
        else:
            visited.add(p)


def main():
    with open("../input/day_1.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1_example1():
    assert part1(parse_input("R2, L3")) == 5


def test_part1_example2():
    assert part1(parse_input("R2, R2, R2")) == 2


def test_part1_example3():
    assert part1(parse_input("R5, L5, R5, R3")) == 12


def test_part2_example1():
    assert part2(parse_input("R8, R4, R4, R8")) == 4
