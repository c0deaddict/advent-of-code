# --- Part Two ---
#
# The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all
# of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's fixed,
#  they're stuck here.
#
# For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers are
# supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights
# of the programs in that tower.
#
# In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same
# weight, and they do: 61.
#
# However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each match.
#  This means that the following sums must all be the same:
#
# ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
# padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
# fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
# As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above
# ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the
# towers balanced. If this change were made, its weight would be 60.
#
# Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?
#


import re
from collections import namedtuple


Program = namedtuple("program", "name weight children")


def find_root(tree):
    candidates = set(tree.keys())
    for program in tree.values():
        for child_name in program.children:
            candidates.remove(child_name)
    return list(candidates)[0]


def calculate_weights(tree, name):
    program = tree[name]
    weight = program.weight
    for child in program.children:
        weight += calculate_weights(tree, child)
    return weight


def search_unbalanced_subtree(tree, name, diff):
    node = tree[name]
    if not len(node.children):
        return name, node.weight - diff

    weights = {child: calculate_weights(tree, child) for child in node.children}
    heaviest = max(weights.values())
    balanced = min(weights.values())

    if heaviest == balanced:
        # Disc is balanced, problem must be in this program's weight.
        return name, node.weight - diff
    else:
        # Children are unbalanced, recurse.
        for child, weight in weights.items():
            if weight == heaviest:
                return search_unbalanced_subtree(tree, child, heaviest - balanced)


def parse_line(line):
    res = re.match("^(\w+) \((\d+)\)(?: -> (\w+(?:, \w+)*))?$", line)
    return Program(
        name=res.group(1),
        weight=int(res.group(2)),
        children=[] if res.group(3) is None else res.group(3).split(", "),
    )


def main():
    with open("../input/day7_1.input.txt") as f:
        tree = {program.name: program for program in [parse_line(line) for line in f]}
        root = find_root(tree)
        print(search_unbalanced_subtree(tree, root, 0))


if __name__ == "__main__":
    main()
