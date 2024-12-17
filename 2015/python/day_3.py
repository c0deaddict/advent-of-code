def parse_input(input):
    return input.strip()


def part1(input):
    x, y = 0, 0
    visited = {(x, y)}
    for move in input:
        match move:
            case "^":
                y -= 1
            case ">":
                x += 1
            case "v":
                y += 1
            case "<":
                x -= 1
        visited.add((x, y))
    return len(visited)


def part2(input):
    pass


def main():
    with open("../input/day_3.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1(">") == 2
    assert part1("^>v<") == 4
    assert part1("^v^v^v^v^v") == 2
