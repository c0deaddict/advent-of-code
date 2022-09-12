import re
from functools import partial


def rect(w, h, image):
    for x in range(w):
        for y in range(h):
            image[x][y] = True


def rotx(x, i, image):
    h = len(image[0])
    col = [image[x][y] for y in range(h)]
    for y in range(h):
        image[x][y] = col[(y - i) % h]


def roty(y, i, image):
    w = len(image)
    row = [image[x][y] for x in range(w)]
    for x in range(w):
        image[x][y] = row[(x - i) % w]


def parse_instr(line):
    i = list(map(int, re.findall(r"\d+", line)))
    if line.startswith("rect "):
        return partial(rect, *i)
    elif line.startswith("rotate row "):
        return partial(roty, *i)
    elif line.startswith("rotate column "):
        return partial(rotx, *i)


def parse_input(input):
    return list(map(parse_instr, input.strip().splitlines()))


def new_image(w, h):
    return [[False] * h for i in range(w)]


def print_image(image):
    for y in range(len(image[0])):
        print("".join("#" if image[x][y] else "." for x in range(len(image))))


def run(input, w, h):
    image = new_image(w, h)
    for instr in input:
        instr(image)
    return image


def pixels_lit(image):
    return sum(1 for col in image for cell in col if cell)


def part1(input):
    return pixels_lit(run(input, 50, 6))


def part2(input):
    print_image(run(input, 50, 6))


def main():
    with open("../input/day_8.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""


def test_part1():
    image = run(parse_input(EXAMPLE_1), 7, 3)
    assert pixels_lit(image) == 6
