def parse_input(input):
    return list(map(int, input.strip()))


def populate_blocks(input):
    blocks = [-1] * sum(input)
    i = 0
    for j, size in enumerate(input):
        if j % 2 == 0:
            for k in range(size):
                blocks[i + k] = j // 2
                pass
        i += size
    return blocks


def checksum(blocks):
    return sum(i * file_id for i, file_id in enumerate(blocks) if file_id >= 0)


def part1(input):
    blocks = populate_blocks(input)
    tail = len(blocks) - 1
    for i in range(len(blocks)):
        if i >= tail:
            break
        if blocks[i] >= 0:
            continue
        blocks[i] = blocks[tail]
        blocks[tail] = -1
        while blocks[tail] < 0:
            tail -= 1

    return checksum(blocks)


def part2(input):
    files = []
    free_space = []
    offset = 0
    for i, size in enumerate(input):
        if i % 2 == 0:
            files.append((offset, size))
        else:
            free_space.append((offset, size))
        offset += size

    checksum = 0
    for file_id, (offset, size) in reversed(list(enumerate(files))):
        for i, (free_offset, free_size) in enumerate(free_space):
            if free_offset > offset:
                break
            if free_size >= size:
                offset = free_offset
                free_size -= size
                if free_size == 0:
                    del free_space[i]
                else:
                    free_space[i] = (free_offset + size, free_size)
                break

        checksum += sum(file_id * (offset + i) for i in range(size))

    return checksum


def main():
    with open("../input/day_9.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
2333133121414131402
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 1928


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 2858
