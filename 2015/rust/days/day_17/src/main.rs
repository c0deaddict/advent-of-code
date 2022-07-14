use itertools::Itertools;
use lib::run;

type Input = Vec<usize>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| l.parse().unwrap())
        .sorted()
        .collect()
}

fn combinations(
    containers: &[usize],
    amount: usize,
    path: Vec<usize>,
    limit: Option<usize>,
) -> Vec<Vec<usize>> {
    if limit.is_some() && path.len() > limit.unwrap() {
        return vec![];
    }

    if amount == 0 {
        return vec![path];
    }

    let mut res = vec![];
    for (i, size) in containers.iter().enumerate() {
        if amount >= *size {
            let path = [path.clone(), vec![*size]].concat();
            res.extend(combinations(
                &containers[(i + 1)..],
                amount - size,
                path,
                limit,
            ));
        }
    }

    res
}

fn part_01(input: &Input) -> usize {
    combinations(input, 150, vec![], None).len()
}

fn min_combinations(containers: &[usize], amount: usize) -> usize {
    let limit = combinations(containers, amount, vec![], None)
        .iter()
        .min_by_key(|p| p.len())
        .unwrap()
        .len();

    combinations(containers, amount, vec![], Some(limit)).len()
}

fn part_02(input: &Input) -> usize {
    min_combinations(input, 150)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    20
    15
    10
    5
    5 
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(combinations(&input, 25, vec![], None).len(), 4)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(min_combinations(&input, 25), 3)
    }
}
