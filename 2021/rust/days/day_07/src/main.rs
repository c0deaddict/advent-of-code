use itertools::Itertools;
use lib::run;
use std::cmp;

type Input = Vec<i32>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .split(",")
        .map(|s| s.parse().unwrap())
        .sorted()
        .collect()
}

fn compute_fuel(input: &Input, pos: i32) -> i32 {
    input.iter().map(|d| (d - pos).abs()).sum()
}

fn part_01(input: &Input) -> i32 {
    let n = input.len();
    if n % 2 == 1 {
        compute_fuel(input, input[(n + 1) / 2])
    } else {
        cmp::min(
            compute_fuel(input, input[n / 2]),
            compute_fuel(input, input[n / 2 + 1]),
        )
    }
}

fn compute_fuel_part2(input: &Input, pos: i32) -> i32 {
    input
        .iter()
        .map(|x| {
            let d = (x - pos).abs();
            (d * (d + 1)) / 2
        })
        .sum()
}

fn part_02(input: &Input) -> i32 {
    let min = *input.first().unwrap();
    let max = *input.last().unwrap();
    (min..=max)
        .map(|i| compute_fuel_part2(input, i as i32))
        .min()
        .unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    16,1,2,0,4,2,7,1,2,14
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 37)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 168)
    }
}
