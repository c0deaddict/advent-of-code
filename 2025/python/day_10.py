def parse_line(line):
    lights = None
    buttons = []
    joltage = None
    for chunk in line.split():
        if chunk[0] == "[":
            lights = tuple(c == "#" for c in chunk[1:-1])
        elif chunk[0] == "(":
            buttons.append(tuple(map(int, chunk[1:-1].split(","))))
        elif chunk[0] == "{":
            joltage = tuple(map(int, chunk[1:-1].split(",")))
    return lights, buttons, joltage


def parse_input(input):
    return [parse_line(line) for line in input.strip().splitlines()]


def press_buttons(lights, bset):
    result = list(lights)
    for b in bset:
        result[b] = not result[b]
    return tuple(result)


def find_fewest_presses(pattern, buttons, _joltage):
    queue = [(0, tuple([False] * len(pattern)))]
    visited = set()
    while True:
        steps, lights = queue.pop(0)
        if lights == pattern:
            return steps
        if lights in visited:
            continue
        visited.add(lights)
        for bset in buttons:
            queue.append((steps + 1, press_buttons(lights, bset)))


def part1(input):
    return sum(find_fewest_presses(*line) for line in input)


def minmax(buttons, joltage):
    maxs = [min(joltage[i] for i in bset) for bset in buttons]
    mins = [
        max(
            0,
            *[
                joltage[j]
                - sum(
                    maxs[k] for k, other in enumerate(buttons) if k != i and j in other
                )
                for j in bset
            ],
        )
        for i, bset in enumerate(buttons)
    ]
    return mins, maxs


def find_fewest_joltage_presses(_lights, buttons, joltage):
    target = [0] * len(joltage)

    best = None

    def loop(buttons, joltage, count):
        nonlocal best

        if joltage == target:
            return count
        if not buttons:
            return
        if best is not None and count + max(joltage) >= best:
            return

        mins, maxs = minmax(buttons, joltage)
        if any(a > b for a, b in zip(mins, maxs)):
            return

        bmin, bmax, bset = min(
            zip(mins, maxs, buttons), key=lambda t: (t[1] - t[0], -len(t[2]))
        )

        next_joltage = list(joltage)
        next_buttons = list(buttons)
        next_buttons.remove(bset)

        for i in range(bmax, bmin - 1, -1):
            for j in bset:
                next_joltage[j] = joltage[j] - i
            next_count = loop(next_buttons, next_joltage, count + i)
            if next_count is not None:
                if best is None or next_count < best:
                    best = next_count

        return best

    result = loop(buttons, joltage, 0)
    assert result is not None
    return result


def print_eq(buttons, joltage):
    components = [
        set(j for j, bset in enumerate(buttons) if i in bset)
        for i, _ in enumerate(joltage)
    ]

    for i, v in enumerate(joltage):
        cs = ("x" + str(c) for c in sorted(components[i]))
        print(f"{v:3d} = {" + ".join(cs)}")


def part2(input):
    total = 0
    for i, line in enumerate(
        sorted(input, key=lambda t: (sum(len(bset) for bset in t[1]), sum(t[2])))[:]
    ):
        _lights, buttons, joltage = line
        print_eq(buttons, joltage)
        result = find_fewest_joltage_presses(*line)
        print(f"----\n#{i} = {result}")
        total += result
        print(f"total = {total}\n")

    return total


def main():
    with open("../input/day_10.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 7


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 33
