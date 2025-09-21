from dataclasses import dataclass
from collections.abc import Callable
import operator


@dataclass
class Gate:
    left: str
    op: str
    right: str
    output: str

    def fn(self) -> Callable[[int, int], int]:
        match self.op:
            case "and":
                return operator.and_
            case "or":
                return operator.or_
            case "xor":
                return operator.xor
            case _:
                raise AssertionError("unknown operator")

    def run(self, wires: dict[str, int]) -> int:
        return self.fn()(wires[self.left], wires[self.right])


def parse_input(input):
    init_lines, gate_lines = input.strip().split("\n\n", 2)

    init = {}
    for line in init_lines.strip().splitlines():
        key, value = line.split(": ", 2)
        init[key] = int(value)

    gates = []
    for line in gate_lines.strip().splitlines():
        left, op, right, _, output = line.split()
        gates.append(Gate(left, op.lower(), right, output))

    return init, gates


def part1(input):
    init, gates = input
    wires = dict(init)
    done = False
    while not done:
        done = True
        for g in gates:
            if g.output in wires:
                continue
            if g.left in wires and g.right in wires:
                wires[g.output] = g.run(wires)
                done = False

    z = "".join(
        str(v) for k, v in sorted(wires.items(), reverse=True) if k.startswith("z")
    )
    return int(z, 2)


def part2(input):
    pass


def main():
    with open("../input/day_24.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_1 = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

EXAMPLE_2 = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


def test_part1_example1():
    assert part1(parse_input(EXAMPLE_1)) == 4


def test_part1_example2():
    assert part1(parse_input(EXAMPLE_2)) == 2024
