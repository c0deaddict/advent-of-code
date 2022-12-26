import operator


def parse_op(op):
    match op:
        case "+":
            return operator.add
        case "-":
            return operator.sub
        case "/":
            return operator.floordiv
        case "*":
            return operator.mul


def parse_line(line):
    monkey, expr = line.split(": ")
    if expr.isdigit():
        return monkey, int(expr)
    lhs, op, rhs = expr.split(" ")
    return monkey, (lhs, parse_op(op), rhs)


def parse_input(input):
    return dict(parse_line(line) for line in input.strip().splitlines())


def solve(input, monkey):
    expr = input[monkey]
    if type(expr) is int:
        return expr
    lhs, op, rhs = expr
    return op(solve(input, lhs), solve(input, rhs))


def part1(input):
    return solve(input, "root")


def inverse_op(op):
    match op:
        case operator.add:
            return operator.sub
        case operator.sub:
            return operator.add
        case operator.mul:
            return operator.floordiv
        case operator.floordiv:
            return operator.mul


def solve_symbolic(input, monkey, var):
    if monkey == var:
        return lambda x: x
    expr = input[monkey]
    if type(expr) is int:
        return expr
    lhs, op, rhs = expr
    match solve_symbolic(input, lhs, var), solve_symbolic(input, rhs, var):
        case int(l), int(r):
            return op(l, r)
        case int(l), r:
            if op == operator.floordiv:
                return lambda x: r(l // x)
            elif op == operator.sub:
                return lambda x: r(l - x)
            else:
                return lambda x: r(inverse_op(op)(x, l))
        case l, int(r):
            return lambda x: l(inverse_op(op)(x, r))


def part2(input):
    lhs, _, rhs = input["root"]
    l = solve_symbolic(input, lhs, "humn")
    r = solve_symbolic(input, rhs, "humn")
    return l(r) if type(r) is int else r(l)


def main():
    with open("../input/day_21.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_1)) == 152


def test_part2():
    assert part2(parse_input(EXAMPLE_1)) == 301
