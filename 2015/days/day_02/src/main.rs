use itertools::Itertools;
use lib::run;
use std::cmp;

type Box = (usize, usize, usize);
type Input = Vec<Box>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            l.splitn(3, "x")
                .map(|d| d.parse().unwrap())
                .sorted()
                .collect_tuple()
                .unwrap()
        })
        .collect()
}

fn paper_area(b: &Box) -> usize {
    let a1 = b.0 * b.1;
    let a2 = b.1 * b.2;
    let a3 = b.0 * b.2;
    2 * a1 + 2 * a2 + 2 * a3 + cmp::min(a1, cmp::min(a2, a3))
}

fn part_01(input: &Input) -> usize {
    input.iter().map(paper_area).sum()
}

fn ribbon_length(b: &Box) -> usize {
    let bow = b.0 * b.1 * b.2;
    2 * b.0 + 2 * b.1 + bow
}

fn part_02(input: &Input) -> usize {
    input.iter().map(ribbon_length).sum()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    2x3x4
    1x1x10";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 58 + 43)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 34 + 14)
    }
}
