use lib::run;
use regex::Regex;
use std::collections::HashMap;
use std::fmt::Debug;

#[derive(Debug)]
struct BitMask {
    mask_and: u64,
    mask_or: u64,
}

#[derive(Debug)]
enum Op {
    Mask(BitMask),
    Mem { addr: u64, val: u64 },
}

type Input = Vec<Op>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"mask = ([X01]+)|mem\[(\d+)\] = (\d+)").unwrap();

    input
        .trim()
        .lines()
        .map(|line| {
            let c = re.captures(line).unwrap();
            if let Some(mask) = c.get(1) {
                let mask = mask.as_str();
                let mask_and = mask.replace('1', "0").replace('X', "1");
                let mask_and = u64::from_str_radix(&mask_and, 2).unwrap();
                let mask_or = mask.replace('X', "0");
                let mask_or = u64::from_str_radix(&mask_or, 2).unwrap();
                Op::Mask(BitMask { mask_and, mask_or })
            } else {
                let addr = c[2].parse().unwrap();
                let val = c[3].parse().unwrap();
                Op::Mem { addr, val }
            }
        })
        .collect()
}

fn part1(input: &Input) -> u64 {
    let mut it = input.iter();
    let mut mask = match it.next().unwrap() {
        Op::Mask(mask) => mask,
        _ => panic!("expected a mask first"),
    };

    let mut mem = HashMap::new();
    for op in input {
        match op {
            Op::Mem { addr, val } => {
                let val = (val & mask.mask_and) | mask.mask_or;
                mem.insert(addr, val);
            }
            Op::Mask(new_mask) => {
                mask = new_mask;
            }
        };
    }

    mem.values().sum()
}

fn bits(mask: u64) -> Vec<u8> {
    let mut result = vec![];
    for i in 0..64 {
        if (mask & (1 << i)) != 0 {
            result.push(i);
        }
    }
    result
}

fn enumerate_addrs(addr: u64, mask: u64) -> Vec<u64> {
    let mask_bits = bits(mask);
    let mut addrs = vec![];
    let mut queue = vec![(addr & !mask, &mask_bits[..])];
    while let Some((addr, mask_bits)) = queue.pop() {
        if let Some(bit) = mask_bits.first() {
            let mask_bits = &mask_bits[1..];
            queue.push((addr, mask_bits));
            queue.push((addr | (1 << bit), mask_bits));
        } else {
            addrs.push(addr);
        }
    }
    addrs
}

fn part2(input: &Input) -> u64 {
    let mut it = input.iter();
    let mut mask = match it.next().unwrap() {
        Op::Mask(mask) => mask,
        _ => panic!("expected a mask first"),
    };

    let mut mem = HashMap::new();

    for op in it {
        match op {
            Op::Mem { addr, val } => {
                for a in enumerate_addrs(addr | mask.mask_or, mask.mask_and) {
                    mem.insert(a, *val);
                }
            }
            Op::Mask(new_mask) => {
                mask = new_mask;
            }
        };
    }

    mem.values().sum()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0";

    const EXAMPLE_DATA_2: &'static str = "
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1";

    const EXAMPLE_DATA_3: &'static str = "
    mask = 00000000000000000000000000000000XXXX
    mem[0] = 1
    mask = 00000000000000000000000000000000XXX0
    mem[0] = 2
    mask = 00000000000000000000000000000000X1XX
    mem[0] = 3
    mask = 00000000000000000000000000000000XX11
    mem[0] = 4";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 165);
    }

    #[test]
    fn example_2_part2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part2(&input), 208);
    }

    #[test]
    fn example_3_part2() {
        let input = parse_input(EXAMPLE_DATA_3);
        assert_eq!(part2(&input), 44);
    }
}
