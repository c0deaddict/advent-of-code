use itertools::Itertools;
use lib::run;
use std::collections::HashMap;

#[derive(Debug, PartialEq, Clone)]
enum Operation {
    Const,
    And,
    Or,
    Not,
    ShiftLeft,
    ShiftRight,
}

#[derive(Debug, Clone)]
struct Gate<'a> {
    op: Operation,
    in0: &'a str,
    in1: Option<&'a str>,
    out: &'a str,
}

impl<'a> Gate<'a> {
    fn new(op: Operation, in0: &'a str, in1: Option<&'a str>, out: &'a str) -> Self {
        Gate { op, in0, in1, out }
    }

    fn inputs(&'a self) -> Vec<&'a str> {
        let mut res = vec![];
        if self.in0.parse::<u16>().is_err() {
            res.push(self.in0);
        }
        if let Some(in1) = self.in1 {
            if in1.parse::<u16>().is_err() {
                res.push(in1);
            }
        }
        res
    }

    fn eval_input(wires: &HashMap<&'a str, u16>, wire: &'a str) -> u16 {
        wire.parse().unwrap_or_else(|_| *wires.get(wire).unwrap())
    }

    fn compute(&'a self, wires: &HashMap<&'a str, u16>) -> u16 {
        match self.op {
            Operation::Const => Self::eval_input(wires, self.in0),
            Operation::And | Operation::Or => {
                let val0 = Self::eval_input(wires, self.in0);
                let val1 = Self::eval_input(wires, self.in1.unwrap());
                if self.op == Operation::And {
                    val0 & val1
                } else {
                    val0 | val1
                }
            }
            Operation::Not => !Self::eval_input(wires, self.in0),
            Operation::ShiftLeft | Operation::ShiftRight => {
                let val0 = Self::eval_input(wires, self.in0);
                let shift: u16 = self.in1.unwrap().parse().unwrap();
                if self.op == Operation::ShiftLeft {
                    val0 << shift
                } else {
                    val0 >> shift
                }
            }
        }
    }
}

type Input<'a> = Vec<Gate<'a>>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let (l, out) = l.splitn(2, " -> ").collect_tuple().unwrap();
            match l.split_whitespace().collect::<Vec<_>>().as_slice() {
                [val] => Gate::new(Operation::Const, val, None, out),
                ["NOT", in0] => Gate::new(Operation::Not, in0, None, out),
                [in0, "AND", in1] => Gate::new(Operation::And, in0, Some(in1), out),
                [in0, "OR", in1] => Gate::new(Operation::Or, in0, Some(in1), out),
                [in0, "LSHIFT", dist] => Gate::new(Operation::ShiftLeft, in0, Some(dist), out),
                [in0, "RSHIFT", dist] => Gate::new(Operation::ShiftRight, in0, Some(dist), out),
                _ => panic!("invalid input gate definition: {}", l),
            }
        })
        .collect()
}

fn emulate<'a>(input: &'a Input) -> HashMap<&'a str, u16> {
    let mut wires: HashMap<&str, u16> = HashMap::new();
    let mut queue: Vec<&Gate> = input.iter().collect();
    while !queue.is_empty() {
        // drain_filter would be nicer, but is unstable.
        let (resolve, new_queue): (Vec<_>, Vec<_>) = queue
            .into_iter()
            .partition(|gate| gate.inputs().iter().all(|i| wires.contains_key(i)));

        for gate in resolve {
            wires.insert(gate.out, gate.compute(&wires));
        }

        queue = new_queue;
    }

    wires
}

fn part_01(input: &Input) -> u16 {
    *emulate(input).get("a").unwrap()
}

fn part_02(input: &Input) -> u16 {
    let a = emulate(input).get("a").unwrap().to_string();

    // Replace gate "$any -> b" with "$a -> b"
    let mut new_input: Vec<_> = input.iter().cloned().collect();
    for gate in new_input.iter_mut() {
        if gate.op == Operation::Const && gate.out == "b" {
            gate.in0 = &a;
        }
    }

    *emulate(&new_input).get("a").unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    123 -> x
    456 -> y
    x AND y -> d
    x OR y -> e
    x LSHIFT 2 -> f
    y RSHIFT 2 -> g
    NOT x -> h
    NOT y -> i";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        let wires = emulate(&input);
        assert_eq!(*wires.get("d").unwrap(), 72);
        assert_eq!(*wires.get("e").unwrap(), 507);
        assert_eq!(*wires.get("f").unwrap(), 492);
        assert_eq!(*wires.get("g").unwrap(), 114);
        assert_eq!(*wires.get("h").unwrap(), 65412);
        assert_eq!(*wires.get("i").unwrap(), 65079);
        assert_eq!(*wires.get("x").unwrap(), 123);
        assert_eq!(*wires.get("y").unwrap(), 456);
    }
}
