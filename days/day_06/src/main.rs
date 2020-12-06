use lib::run;
use std::collections::HashSet;

type Input = Vec<Vec<HashSet<char>>>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .split("\n\n")
        .map(|g| g.lines().map(|l| l.trim().chars().collect()).collect())
        .collect()
}

fn part_01(input: &Input) -> usize {
    input
        .iter()
        .map(|g| {
            g.iter()
                .fold(HashSet::new(), |mut res: HashSet<char>, val| {
                    res.extend(val.iter());
                    res
                })
                .len()
        })
        .sum()
}

fn part_02(input: &Input) -> usize {
    input
        .iter()
        .map(|g| {
            // NOTE: Nightly has a method `fold_first` on iter, which does
            // exactly what we want here.
            let mut it = g.iter();
            let first: HashSet<char> = it.next().unwrap().iter().cloned().collect();
            it.fold(first, |res, val| &res & val).len()
        })
        .sum()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b";

    #[test]
    fn example_part_01() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 11);
    }

    #[test]
    fn example_part_02() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 6);
    }
}
