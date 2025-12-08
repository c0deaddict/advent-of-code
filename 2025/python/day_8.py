import operator
from functools import reduce
from itertools import islice


def parse_input(input):
    return [
        tuple(int(d) for d in line.split(",")) for line in input.strip().splitlines()
    ]


def distance(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def connect_junction_boxes(input):
    components = []
    closest = sorted(
        ((a, b) for i, a in enumerate(input) for b in input[i + 1 :]),
        key=lambda pair: distance(*pair),
    )

    while closest:
        a, b = closest.pop(0)
        ca, cb = None, None
        for i, c in enumerate(components):
            if a in c:
                ca = i
            if b in c:
                cb = i

        if ca == None and cb == None:
            components.append({a, b})
        elif ca == cb:
            pass  # already connected
        elif ca is not None and cb is not None:
            ca = components[ca]
            cb = components[cb]
            components.append(ca | cb)
            components.remove(ca)
            components.remove(cb)
        elif ca is not None:
            components[ca] = components[ca] | {b}
        elif cb is not None:
            components[cb] = components[cb] | {a}

        yield components, (a, b)


def part1(input, n=1000):
    components, _ = next(islice(connect_junction_boxes(input), n - 1, n))
    return reduce(operator.mul, sorted(map(len, components), reverse=True)[0:3])


def part2(input):
    for components, (a, b) in connect_junction_boxes(input):
        if len(components) == 1 and len(components[0]) == len(input):
            return a[0] * b[0]


def main():
    with open("../input/day_8.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1), 10) == 40


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 25272
