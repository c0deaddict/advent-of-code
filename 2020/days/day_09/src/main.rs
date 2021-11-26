use itertools::Itertools;
use lib::run;

type Input = Vec<u64>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|l| l.trim().parse::<u64>().unwrap())
        .collect()
}

fn find_invalid(input: &Input, preamble: usize) -> u64 {
    input
        .windows(preamble + 1)
        .map(|win| {
            let mut win: Vec<u64> = win.iter().cloned().collect();
            let value = win.pop().unwrap();
            let valid = win
                .iter()
                .combinations(2)
                .map(|v| v[0] + v[1])
                .any(|x| x == value);
            (value, valid)
        })
        .find(|(_win, valid)| !valid)
        .unwrap()
        .0
}

fn part_01(input: &Input) -> u64 {
    find_invalid(input, 25)
}

fn find_weakness(input: &Input, preamble: usize) -> u64 {
    let value = find_invalid(input, preamble);
    for i in 0..input.len() {
        let mut numbers = vec![];
        let mut sum = 0;
        for j in i..input.len() {
            numbers.push(input[j]);
            sum += input[j];
            if sum == value {
                numbers.sort();
                return numbers.first().unwrap() + numbers.last().unwrap();
            } else if sum == value {
                break;
            }
        }
    }
    panic!("encryption weakness not found");
}

fn part_02(input: &Input) -> u64 {
    find_weakness(input, 25)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    35
    20
    15
    25
    47
    40
    62
    55
    65
    95
    102
    117
    150
    182
    127
    219
    299
    277
    309
    576";

    #[test]
    fn example_part_01() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(find_invalid(&input, 5), 127);
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(find_weakness(&input, 5), 62);
    }
}
