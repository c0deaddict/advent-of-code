import re
from collections import Counter
from functools import cmp_to_key


def parse_input(input):
    return [parse_room(line) for line in input.strip().splitlines()]


def parse_room(room):
    return re.match(
        r"^(?P<name>(?:[a-z]+-)+)(?P<sector_id>\d+)\[(?P<checksum>[a-z]+)\]$", room
    ).groupdict()


def verify(room):
    def compare(a, b):
        if a[1] == b[1]:
            # alphabetical sort if frequencies match
            return ord(a[0]) - ord(b[0])
        # reverse sort on frequency
        return b[1] - a[1]

    top = sorted(
        Counter(c for c in room["name"] if c != "-").items(),
        key=cmp_to_key(compare),
    )
    return room["checksum"] == "".join(f[0] for f in top[0:5])


def part1(input):
    return sum(int(room["sector_id"]) for room in filter(verify, input))


def rotate(c, amount):
    i = ord(c) - ord("a")
    i = (i + amount) % 26
    return chr(ord("a") + i)


def decrypt(room):
    return "".join(
        rotate(c, int(room["sector_id"])) if c != "-" else " " for c in room["name"]
    ).strip()


def part2(input):
    for room in input:
        if decrypt(room) == "northpole object storage":
            return room["sector_id"]


def main():
    with open("../input/day_4.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert verify(parse_room("aaaaa-bbb-z-y-x-123[abxyz]"))
    assert verify(parse_room("a-b-c-d-e-f-g-h-987[abcde]"))
    assert verify(parse_room("not-a-real-room-404[oarel]"))
    assert not verify(parse_room("totally-real-room-200[decoy]"))


def test_part2():
    assert decrypt(parse_room("qzmt-zixmtkozy-ivhz-343[a]")) == "very encrypted name"
