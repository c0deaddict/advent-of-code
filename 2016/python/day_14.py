import hashlib
from functools import partial
from itertools import count, islice
from collections import defaultdict


def parse_input(input):
    return input.strip()


def find_seqs(hash, size):
    for i in range(len(hash) - (size - 1)):
        found = True
        for j in range(1, size):
            if hash[i] != hash[i + j]:
                found = False
                break
        if found:
            yield hash[i]


def hash(salt, idx):
    return hashlib.md5(bytes(f"{salt}{idx}", "utf-8")).hexdigest()


def stretched_hash(count, salt, idx):
    h = hash(salt, idx)
    for _ in range(count):
        h = hashlib.md5(bytes(h, "utf-8")).hexdigest()
    return h


def keys(salt, hash_fn):
    def make_hash(salt, idx):
        h = hash_fn(salt, idx)
        return (h, set(find_seqs(h, 5)))

    window = [make_hash(salt, idx) for idx in range(1000)]

    # Keep a dict of quintlets found in the window. We remember the idx so we
    # can remove them when the hash is shifted from the window.
    quintlets = defaultdict(set)
    for idx, (h, quintlets_add) in enumerate(window):
        for ch in quintlets_add:
            quintlets[ch].add(idx)

    for idx in count(start=0):
        h, quintlets_remove = window[idx % 1000]
        for ch in quintlets_remove:
            quintlets[ch].remove(idx)
            if not quintlets[ch]:
                del quintlets[ch]

        window[idx % 1000] = make_hash(salt, idx + 1000)
        for ch in window[idx % 1000][1]:
            quintlets[ch].add(idx + 1000)

        for ch in islice(find_seqs(h, 3), 0, 1):
            if ch in quintlets:
                yield idx


def part1(input):
    return list(islice(keys(input, hash), 0, 64))[-1]


def part2(input):
    hash = partial(stretched_hash, 2016)
    return list(islice(keys(input, hash), 0, 64))[-1]


def main():
    with open("../input/day_14.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert part1("abc") == 22728


def test_part2():
    assert part2("abc") == 22551
