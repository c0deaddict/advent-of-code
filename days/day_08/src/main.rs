use itertools::Itertools;
use lib::run;
use std::collections::{HashMap, HashSet};

enum Instr {
    Acc(i32),
    Jmp(i32),
    Nop,
}

type Input = Vec<Instr>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|l| l.trim())
        .map(|l| {
            let (op, val) = l.splitn(2, " ").collect_tuple().unwrap();
            let val = val.parse::<i32>().unwrap();
            match op {
                "acc" => Instr::Acc(val),
                "jmp" => Instr::Jmp(val),
                "nop" => Instr::Nop,
                _ => panic!("unknown instruction {}", op),
            }
        })
        .collect()
}

fn part_01(input: &Input) -> i32 {
    let mut acc: i32 = 0;
    let mut pc: i32 = 0;
    let mut visited = HashSet::new();
    while true {
        if !visited.insert(pc) {
            break;
        }
        match input[pc as usize] {
            Instr::Acc(i) => {
                acc += i;
                pc += 1;
            }
            Instr::Jmp(i) => pc += i,
            Instr::Nop => pc += 1,
        }
    }
    acc
}

fn part_02(input: &Input) -> i32 {
    let jumps = input
        .iter()
        .enumerate()
        .filter(|(i, instr)| matches!(instr, Instr::Jmp(_)));

    'outer: for (i, _) in jumps {
        let mut acc: i32 = 0;
        let mut pc: i32 = 0;
        let mut visited = HashSet::new();
        while true {
            if pc == input.len() as i32 {
                return acc;
            } else if !visited.insert(pc) {
                continue 'outer;
            }
            let instr = if pc == i as i32 {
                &Instr::Nop
            } else {
                &input[pc as usize]
            };
            match instr {
                Instr::Acc(i) => {
                    acc += i;
                    pc += 1;
                }
                Instr::Jmp(i) => pc += i,
                Instr::Nop => pc += 1,
            }
        }
    }

    panic!("not found");
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6";

    #[test]
    fn example_part_01() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 5);
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 8);
    }
}
