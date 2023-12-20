import re
from functools import reduce
import operator


def parse_rule(s):
    if m := re.match(r"(\w+)([<>])(\d+):(\w+)", s):
        return (m.group(1), m.group(2), int(m.group(3)), m.group(4))
    else:
        return (s,)


def parse_workflow(line):
    id, line = line.split("{", 1)
    rules = [parse_rule(s) for s in line.strip("}").split(",")]
    return id, rules


def parse_part(line):
    for kv in line.strip("{}").split(","):
        k, v = kv.split("=", 1)
        yield k, int(v)


def parse_input(input):
    workflows, parts = input.strip().split("\n\n")
    workflows = dict(parse_workflow(line) for line in workflows.splitlines())
    parts = [dict(parse_part(line)) for line in parts.splitlines()]
    return workflows, parts


def eval(rules, part):
    for rule in rules:
        match rule:
            case (label, "<", value, out):
                if part[label] < value:
                    return out
            case (label, ">", value, out):
                if part[label] > value:
                    return out
            case (out,):
                return out


def accept(workflows, part):
    i = "in"
    while i not in ("A", "R"):
        i = eval(workflows[i], part)
    return i == "A"


def part1(input):
    workflows, parts = input
    return sum(sum(part.values()) for part in parts if accept(workflows, part))


def split_ranges(ranges, label, op, value):
    a, b = ranges[label]
    # left does not match, right matches rule
    left = right = None

    if op == "<":
        if a >= value:
            right = ranges
        elif b < value:
            left = ranges
        else:
            left = ranges | {label: (value, b)}
            right = ranges | {label: (a, value - 1)}
    else:
        if b <= value:
            left = ranges
        elif a > value:
            right = ranges
        else:
            left = ranges | {label: (a, value)}
            right = ranges | {label: (value + 1, b)}

    return left, right


def product(it):
    return reduce(operator.mul, it)


def combinations(workflows, current, ranges):
    if current == "A":
        return product(abs(a - b) + 1 for a, b in ranges.values())

    elif current == "R":
        return 0

    result = 0
    for rule in workflows[current]:
        match rule:
            case (label, op, value, out):
                ranges, right = split_ranges(ranges, label, op, value)
                if right:
                    result += combinations(workflows, out, right)
                if ranges is None:
                    break
            case (out,):
                result += combinations(workflows, out, ranges)
                break
    return result


def part2(input):
    workflows, _ = input
    return combinations(workflows, "in", {c: (1, 4000) for c in "xmas"})


def main():
    with open("../input/day_19.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 19114


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 167409079868000
