def parse_tree(chunks):
    fs = {}
    cwd = []
    for chunk in chunks:
        cmd, *output = chunk.splitlines()
        if cmd.startswith("cd "):
            cd = cmd[3:]
            if cd == "/":
                cwd = []
            elif cd == "..":
                cwd.pop()
            else:
                cwd.append(cd)
        else:
            p = lookup(fs, cwd)
            for line in output:
                match line.split():
                    case ["dir", name]:
                        p[name] = {}
                    case [size, name]:
                        p[name] = int(size)
    return fs


def lookup(fs, cwd):
    p = fs
    for d in cwd:
        p = p[d]
    return p


def parse_input(input):
    return parse_tree(chunk.strip() for chunk in input.strip().split("$ ")[1:])


def traverse(dir):
    for key, value in dir.items():
        yield key, value
        if type(value) is dict:
            yield from traverse(value)


def size(node):
    if type(node) is int:
        return node
    else:
        return sum(size(child) for _, child in node.items())


def part1(input):
    return sum(
        filter(
            lambda s: s <= 100000,
            (size(node) for name, node in traverse(input) if type(node) is dict),
        )
    )


def part2(input):
    free_space = 70000000 - size(input)
    need_space = 30000000 - free_space
    return min(
        filter(
            lambda s: s >= need_space,
            (size(node) for name, node in traverse(input) if type(node) is dict),
        )
    )


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 95437


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 24933642
