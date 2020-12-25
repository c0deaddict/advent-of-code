use lib::run;
use itertools::Itertools;

type Input = (usize, usize);

const ENC_SUBJECT: usize = 7;
const ENC_MOD: usize = 20201227;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|line| line.trim().parse().unwrap())
        .collect_tuple()
        .unwrap()
}

fn find_loop_size(pubkey: usize) -> usize {
    let mut val = 1;
    let mut loop_size = 0;
    while val != pubkey {
        val = (val * ENC_SUBJECT) % ENC_MOD;
        loop_size += 1;
        if loop_size % 100_000_000 == 0 {
            println!("{}", loop_size);
        }
    }
    loop_size
}

fn encryption_key(pubkey: usize, loop_size: usize) -> usize {
    let mut enckey = 1;
    for _ in 0..loop_size {
        enckey = (enckey * pubkey) % ENC_MOD;
    }
    enckey
}

fn part1(input: &Input) -> usize {
    let door_loop_size = find_loop_size(input.1);
    encryption_key(input.0, door_loop_size)
}

fn part2(input: &Input) -> usize {
    0
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    5764801
    17807724";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 14897079);
    }
}
