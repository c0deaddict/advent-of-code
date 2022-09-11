import re
from itertools import chain


def parse_input(input):
    return list(map(parse_network, input.strip().splitlines()))


def parse_network(line):
    return re.split(r"\[|\]", line)


def contains_abba(part):
    for i in range(len(part) - 3):
        if (
            part[i + 0] == part[i + 3]
            and part[i + 1] == part[i + 2]
            and part[i + 0] != part[i + 1]
        ):
            return True
    return False


def support_tls(network):
    # Uneven indices contain hypernet sequences.
    return any(contains_abba(part) for part in network[0::2]) and all(
        not contains_abba(part) for part in network[1::2]
    )


def part1(input):
    return len(list(filter(support_tls, input)))


def find_abas(part):
    for i in range(len(part) - 2):
        if part[i + 0] != part[i + 1] and part[i + 0] == part[i + 2]:
            yield part[i : i + 3]


def support_ssl(network):
    abas = set(chain(*map(find_abas, network[0::2])))
    babs = set(chain(*map(find_abas, network[1::2])))
    return any(a[0] == b[1] and a[1] == b[0] for a in abas for b in babs)


def part2(input):
    return len(list(filter(support_ssl, input)))


def main():
    with open("../input/day_7.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
"""


def test_part1():
    assert support_tls(parse_network("abba[mnop]qrst"))
    assert not support_tls(parse_network("abcd[bddb]xyyx"))
    assert not support_tls(parse_network("aaaa[qwer]tyui"))
    assert support_tls(parse_network("ioxxoj[asdfgh]zxcvbn"))


def test_part2():
    assert support_ssl(parse_network("aba[bab]xyz"))
    assert not support_ssl(parse_network("xyx[xyx]xyx"))
    assert support_ssl(parse_network("aaa[kek]eke"))
    assert support_ssl(parse_network("zazbz[bzb]cdb"))
