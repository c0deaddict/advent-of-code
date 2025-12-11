from collections import defaultdict


def parse_line(line):
    parts = line.split(":", 2)
    return parts[0], parts[1].strip().split()


def parse_input(input):
    return dict(parse_line(line) for line in input.strip().splitlines())


def count_paths(input, start, target):
    count = dict()

    queue = [start]
    while queue:
        v = queue.pop(0)
        if v == target:
            count[v] = 1
            continue

        computed = True
        for n in input.get(v, []):
            if n not in count:
                if n not in queue:
                    queue.append(n)
                computed = False

        if computed:
            count[v] = sum(count[n] for n in input.get(v, []))
        else:
            queue.append(v)

    return count[start]


def part1(input):
    return count_paths(input, "you", "out")


def part2(input):
    return (
        count_paths(input, "svr", "fft")
        * count_paths(input, "fft", "dac")
        * count_paths(input, "dac", "out")
    )


def main():
    with open("../input/day_11.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


EXAMPLE_2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 5


def test_part2():
    assert part2(parse_input(EXAMPLE_2)) == 2
