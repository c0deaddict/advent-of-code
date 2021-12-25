use lib::run;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
enum Register {
    W = 0,
    X,
    Y,
    Z,
}

#[derive(Debug, Copy, Clone)]
enum Argument {
    Register(Register),
    Literal(i64),
}

#[derive(Debug, Copy, Clone)]
enum Instruction {
    Inp(Register),
    Add(Register, Argument),
    Mul(Register, Argument),
    Div(Register, Argument),
    Mod(Register, Argument),
    Eql(Register, Argument),
}

impl Register {
    fn parse(s: &str) -> Option<Self> {
        match s {
            "w" => Some(Self::W),
            "x" => Some(Self::X),
            "y" => Some(Self::Y),
            "z" => Some(Self::Z),
            _ => None,
        }
    }
}

impl Instruction {
    fn parse(s: &str) -> Instruction {
        let mut it = s.split_whitespace();
        let op = it.next().unwrap();
        let reg = Register::parse(it.next().unwrap()).unwrap();
        let arg = it.next().map(|s| match Register::parse(s) {
            Some(reg) => Argument::Register(reg),
            None => Argument::Literal(s.parse().unwrap()),
        });
        match op {
            "inp" => Instruction::Inp(reg),
            "add" => Instruction::Add(reg, arg.unwrap()),
            "mul" => Instruction::Mul(reg, arg.unwrap()),
            "div" => Instruction::Div(reg, arg.unwrap()),
            "mod" => Instruction::Mod(reg, arg.unwrap()),
            "eql" => Instruction::Eql(reg, arg.unwrap()),
            _ => panic!("unknown opcode {}", op),
        }
    }

    fn target(&self) -> Register {
        match self {
            Self::Inp(reg) => *reg,
            Self::Add(reg, _) => *reg,
            Self::Mul(reg, _) => *reg,
            Self::Div(reg, _) => *reg,
            Self::Mod(reg, _) => *reg,
            Self::Eql(reg, _) => *reg,
        }
    }
}

struct RegisterMap([i64; 4]);

impl RegisterMap {
    fn new() -> Self {
        RegisterMap([0; 4])
    }

    fn get(&self, reg: Register) -> i64 {
        self.0[reg as usize]
    }

    fn set(&mut self, reg: Register, value: i64) {
        self.0[reg as usize] = value;
    }
}

type Input = Vec<Instruction>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| Instruction::parse(l))
        .collect()
}

#[inline(always)]
fn eval_arg(regs: &RegisterMap, arg: &Argument) -> i64 {
    match arg {
        Argument::Register(reg) => regs.get(*reg),
        Argument::Literal(value) => *value,
    }
}

fn run_program(program: &Input, regs: &mut RegisterMap, input_stack: &mut Vec<i64>) {
    for instr in program {
        let value = match instr {
            Instruction::Inp(_) => input_stack.pop().unwrap(),
            Instruction::Add(reg, arg) => regs.get(*reg) + eval_arg(&regs, arg),
            Instruction::Mul(reg, arg) => regs.get(*reg) * eval_arg(&regs, arg),
            Instruction::Div(reg, arg) => regs.get(*reg) / eval_arg(&regs, arg),
            Instruction::Mod(reg, arg) => regs.get(*reg) % eval_arg(&regs, arg),
            Instruction::Eql(reg, arg) => {
                if regs.get(*reg) == eval_arg(&regs, arg) {
                    1
                } else {
                    0
                }
            }
        };
        regs.set(instr.target(), value);
    }
}

fn split_program_on_inputs(program: &Input) -> Vec<Input> {
    let mut res = vec![];
    let mut current = vec![];
    for instr in program {
        if let Instruction::Inp(_) = instr {
            res.push(current);
            current = vec![];
        }
        current.push(*instr);
    }
    res.remove(0);
    res.push(current);
    return res;
}

fn run_sub_program(program: &Input, digit: i64, in_z: i64) -> i64 {
    let mut regs = RegisterMap::new();
    regs.set(Register::Z, in_z);
    let mut input = vec![digit];
    run_program(&program, &mut regs, &mut input);
    return regs.get(Register::Z);
}

fn assemble_digits(digits: Vec<i64>) -> i64 {
    // Digits are in wrong order, i.e. highest number first.
    let mut res = 0;
    for d in digits.iter().rev() {
        res = res * 10 + d;
    }
    return res;
}

fn assemble_model_numbers(
    mapping: &HashMap<(usize, i64), Vec<(i64, i64)>>,
    stage: usize,
    out_z: i64,
    digits: Vec<i64>,
    results: &mut Vec<i64>,
) {
    for (in_z, digit) in mapping.get(&(stage, out_z)).unwrap() {
        let mut digits = digits.clone();
        digits.push(*digit);
        if stage == 0 {
            results.push(assemble_digits(digits));
        } else {
            assemble_model_numbers(&mapping, stage - 1, *in_z, digits, results);
        }
    }
}

fn compute_model_numbers(input: &Input) -> Vec<i64> {
    let mut mapping = HashMap::new();

    // Split the program on input points. Each sub program is only reliant on
    // the Z value produced by the previous program, and the input value.
    let mut prev_z: HashSet<_> = vec![0].iter().cloned().collect();
    for (stage, program) in split_program_on_inputs(&input).iter().enumerate() {
        let mut next_z = HashSet::new();

        for in_z in prev_z {
            for digit in 1..=9 {
                let out_z = run_sub_program(&program, digit, in_z);

                // Each stage can at most divide Z by 26. So if the out_z value
                // exceeds 26^remaining_stages it can be skipped.
                if out_z > (26 as i64).pow((13 - stage) as u32) {
                    continue;
                }

                // Keep a mapping per stage between the out_z and (in_z, digit).
                mapping
                    .entry((stage, out_z))
                    .or_insert_with(|| vec![])
                    .push((in_z, digit));

                // Build the set of next_z values. There are a lot of duplicates
                // here hence the HashSet.
                next_z.insert(out_z);
            }
        }

        prev_z = next_z;
    }

    // Work backwards from the mapping starting at stage 13 with out_z = 0.
    let mut results = vec![];
    assemble_model_numbers(&mapping, 13, 0, vec![], &mut results);
    return results;
}

fn part_01(input: &Input) -> i64 {
    *compute_model_numbers(&input).iter().max().unwrap()
}

fn part_02(input: &Input) -> i64 {
    *compute_model_numbers(&input).iter().min().unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}
