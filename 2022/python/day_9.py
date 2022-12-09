from dataclasses import dataclass


def sign(v):
    return 1 if v > 0 else -1


@dataclass
class Point:
    x: int
    y: int

    def step(self, dir):
        match dir:
            case "R":
                self.x += 1
            case "L":
                self.x -= 1
            case "U":
                self.y -= 1
            case "D":
                self.y += 1

    def follow(self, head):
        match (head.x - self.x, head.y - self.y):
            case (0, dy) if abs(dy) > 1:
                self.y += sign(dy)
            case (dx, 0) if abs(dx) > 1:
                self.x += sign(dx)
            case (dx, dy) if abs(dx) + abs(dy) > 2:
                self.x += sign(dx)
                self.y += sign(dy)


def parse_input(input):
    return [line.split() for line in input.strip().splitlines()]


def part1(input):
    visited = set()
    head = Point(0, 0)
    tail = Point(0, 0)
    for dir, count in input:
        for _ in range(int(count)):
            head.step(dir)
            tail.follow(head)
            visited.add((tail.x, tail.y))
    return len(visited)


def part2(input):
    visited = set()
    rope = [Point(0, 0) for _ in range(10)]
    for dir, count in input:
        for _ in range(int(count)):
            rope[0].step(dir)
            for i in range(1, len(rope)):
                rope[i].follow(rope[i - 1])
            visited.add((rope[-1].x, rope[-1].y))
    return len(visited)


def main():
    with open("../input/day_9.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 13


EXAMPLE_2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 1
    assert part2(parse_input(EXAMPLE_2)) == 36
