use std::collections::HashSet;

use lazy_static::lazy_static;
use lib::run;
use regex::Regex;

enum Operation {
    TurnOn,
    Toggle,
    TurnOff,
}

#[derive(PartialEq, Eq, Hash, Clone)]
struct Position {
    x: usize,
    y: usize,
}

struct Instruction {
    op: Operation,
    from: Position,
    to: Position,
}

type Input = Vec<Instruction>;

lazy_static! {
    static ref INSTRUCTION_RE: Regex =
        Regex::new(r"^(turn on|toggle|turn off) (\d+),(\d+) through (\d+),(\d+)$").unwrap();
}

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let c = INSTRUCTION_RE.captures(l).unwrap();
            let op = match c.get(1).unwrap().as_str() {
                "turn on" => Operation::TurnOn,
                "toggle" => Operation::Toggle,
                "turn off" => Operation::TurnOff,
                op => panic!("unknown operation {}", op),
            };
            let from = Position {
                x: c.get(2).unwrap().as_str().parse().unwrap(),
                y: c.get(3).unwrap().as_str().parse().unwrap(),
            };
            let to = Position {
                x: c.get(4).unwrap().as_str().parse().unwrap(),
                y: c.get(5).unwrap().as_str().parse().unwrap(),
            };
            Instruction { op, from, to }
        })
        .collect()
}

fn part_01(input: &Input) -> usize {
    let mut lights = vec![false; 1000 * 1000];
    for instr in input {
        for x in instr.from.x..instr.to.x + 1 {
            for y in instr.from.y..instr.to.y + 1 {
                let idx = x + y * 1000;
                match instr.op {
                    Operation::TurnOn => lights[idx] = true,
                    Operation::Toggle => lights[idx] = !lights[idx],
                    Operation::TurnOff => lights[idx] = false,
                };
            }
        }
    }

    lights.iter().filter(|v| **v).count()
}

fn part_02(input: &Input) -> usize {
    let mut lights = vec![0; 1000 * 1000];
    for instr in input {
        for x in instr.from.x..instr.to.x + 1 {
            for y in instr.from.y..instr.to.y + 1 {
                let idx = x + y * 1000;
                match instr.op {
                    Operation::TurnOn => lights[idx] += 1,
                    Operation::Toggle => lights[idx] += 2,
                    Operation::TurnOff => {
                        lights[idx] = if lights[idx] > 0 {
                            lights[idx] - 1
                        } else {
                            lights[idx]
                        }
                    }
                };
            }
        }
    }

    lights.iter().sum()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    turn on 0,0 through 999,999
    toggle 0,0 through 999,0
    turn off 499,499 through 500,500
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 998996)
    }

    const EXAMPLE_DATA_2: &'static str = "
    turn on 0,0 through 0,0
    toggle 0,0 through 999,999
    ";

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_02(&input), 2000001)
    }
}
