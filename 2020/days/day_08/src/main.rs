use itertools::Itertools;
use lib::run;
use std::collections::HashSet;

enum Instr {
    Acc(i32),
    Jmp(i32),
    Nop(i32),
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
                "nop" => Instr::Nop(val),
                _ => panic!("unknown instruction {}", op),
            }
        })
        .collect()
}

fn part_01(input: &Input) -> i32 {
    let mut acc: i32 = 0;
    let mut pc: i32 = 0;
    let mut visited = HashSet::new();
    loop {
        if !visited.insert(pc) {
            break;
        }
        match input[pc as usize] {
            Instr::Acc(i) => {
                acc += i;
                pc += 1;
            }
            Instr::Jmp(i) => pc += i,
            Instr::Nop(_) => pc += 1,
        }
    }
    acc
}

fn part_02(input: &Input) -> i32 {
    let jumps_and_nops = input.iter().enumerate().filter(|(_, instr)| match instr {
        Instr::Jmp(_) => true,
        Instr::Nop(_) => true,
        _ => false,
    });

    'outer: for (change_pc, _) in jumps_and_nops {
        let mut acc: i32 = 0;
        let mut pc: i32 = 0;
        let mut visited = HashSet::new();
        loop {
            if pc == input.len() as i32 {
                return acc;
            } else if !visited.insert(pc) {
                continue 'outer;
            }

            let instr = &input[pc as usize];
            // Reverse Jmp and Nop instructions.
            if pc == change_pc as i32 {
                match instr {
                    Instr::Acc(i) => {
                        acc += i;
                        pc += 1;
                    }
                    Instr::Nop(i) => pc += i,
                    Instr::Jmp(_) => pc += 1,
                }
            } else {
                match instr {
                    Instr::Acc(i) => {
                        acc += i;
                        pc += 1;
                    }
                    Instr::Jmp(i) => pc += i,
                    Instr::Nop(_) => pc += 1,
                }
            };
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
