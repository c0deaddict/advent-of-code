# --- Day 7: Recursive Circus ---
#
# Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves
# into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large
# tower.
#
# One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several
# more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding
# their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the
# disc below them balanced but with no disc of their own.
#
# You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out
# their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing
# on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this
# in an orderly fashion; by the time you're done, you're not sure which program gave which information.
#
# For example, if your list is the following:
#
# pbga (66)
# xhth (57)
# ebii (61)
# havc (66)
# ktlj (57)
# fwft (72) -> ktlj, cntj, xhth
# qoyq (66)
# padx (45) -> pbga, havc, qoyq
# tknk (41) -> ugml, padx, fwft
# jptl (61)
# ugml (68) -> gyxo, ebii, jptl
# gyxo (61)
# cntj (57)
# ...then you would be able to recreate the structure of the towers that looks like this:
#
#                 gyxo
#               /
#          ugml - ebii
#        /      \
#       |         jptl
#       |
#       |         pbga
#      /        /
# tknk --- padx - havc
#      \        \
#       |         qoyq
#       |
#       |         ktlj
#        \      /
#          fwft - cntj
#               \
#                 xhth
# In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft.
# Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up any
# other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much larger.)
#
# Before you're ready to help them, you need to make sure your information is correct. What is the name of the bottom
# program?

import re
from collections import namedtuple


Program = namedtuple("program", "name weight children")


def find_root(input):
    candidates = set([program.name for program in input])
    for program in input:
        for child_name in program.children:
            candidates.remove(child_name)
    return list(candidates)[0]


def parse_line(line):
    res = re.match("^(\w+) \((\d+)\)(?: -> (\w+(?:, \w+)*))?$", line)
    return Program(
        name=res.group(1),
        weight=int(res.group(2)),
        children=[] if res.group(3) is None else res.group(3).split(", "),
    )


def main():
    with open("../input/day7_1.input.txt") as f:
        print(find_root([parse_line(line) for line in f]))


if __name__ == "__main__":
    main()
