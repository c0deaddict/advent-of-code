import pytest
from collections import defaultdict
from functools import cmp_to_key

def parse_input(input):
    return [
        tuple(map(int, s.split('/', 2)))
        for s in input.strip().splitlines()
    ]

def connections(input):
    conns = defaultdict(list)
    for (a, b) in input:
        conns[a].append(b)
        conns[b].append(a)
    return conns

def enumerate_bridges(pipes):
    queue = [([0], set())]
    results = []
    while len(queue):
        (bridge, visited) = queue.pop()
        for i, (a, b) in enumerate(pipes):
            if i not in visited and bridge[-1] in (a, b):
                new_visited = visited | {i}
                other = a if bridge[-1] == b else b
                new_bridge = bridge + [bridge[-1], other]
                queue.append((new_bridge, new_visited))
                results.append(new_bridge)
    return results

def part1(input):
    return max(map(sum, enumerate_bridges(input)))

def part2(input):
    def compare_length_and_strength(a, b):
        if len(a) != len(b):
            return len(a) - len(b)
        else:
            return sum(a) - sum(b)
    return sum(max(enumerate_bridges(input), key=cmp_to_key(compare_length_and_strength)))

def main():
    with open('../input/day_24.txt', 'r') as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))

if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""

def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 31

def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_1)) == 19
