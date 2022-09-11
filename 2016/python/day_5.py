import hashlib
from itertools import count, islice


def parse_input(input):
    return input.strip()


def find_hashes(door):
    for i in count(start=0):
        hash = hashlib.md5(bytes(f"{door}{i}", "utf-8")).hexdigest()
        if hash.startswith("00000"):
            yield hash


def part1(input):
    return "".join(h[5] for h in islice(find_hashes(input), 8))


def part2(input):
    password = {}
    for hash in find_hashes(input):
        i = int(hash[5], 16)
        if i < 8 and i not in password:
            password[i] = hash[6]
            if len(password) == 8:
                return "".join(c for _, c in sorted(password.items()))


def main():
    with open("../input/day_5.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1("abc") == "18f47a30"


def test_part2():
    assert part2("abc") == "05ace8e3"
