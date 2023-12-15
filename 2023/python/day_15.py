def parse_input(input):
    return input.strip().split(",")


def hash(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h


def part1(input):
    return sum(map(hash, input))


def find_lens(box, label):
    for i, (lens, _) in enumerate(box):
        if lens == label:
            return i
    return None


def part2(input):
    boxes = [[] for _ in range(256)]
    for s in input:
        if s.endswith("-"):
            label = s[:-1]
            box = boxes[hash(label)]
            if (i := find_lens(box, label)) is not None:
                del box[i]
        else:
            label, fl = s.split("=")
            box = boxes[hash(label)]
            if (i := find_lens(box, label)) is not None:
                box[i][1] = fl
            else:
                box.append([label, fl])

    return sum(
        (1 + i) * slot * int(fl)
        for i, box in enumerate(boxes)
        for slot, (_, fl) in enumerate(box, 1)
    )


def main():
    with open("../input/day_15.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 1320


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 145
