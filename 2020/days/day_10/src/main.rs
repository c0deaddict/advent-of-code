use itertools::Itertools;
use lib::run;
use std::collections::HashMap;

type Input = Vec<u64>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|l| l.trim().parse::<u64>().unwrap())
        .collect()
}

fn diffs(input: &Input) -> Vec<u64> {
    input
        .iter()
        .sorted()
        .fold((0, vec![]), |(a, mut diffs), b| {
            diffs.push(b - a);
            (*b, diffs)
        })
        .1
}

fn part_01(input: &Input) -> u64 {
    let counts = diffs(input).iter().fold([0, 0, 0], |mut counts, d| {
        counts[(d - 1) as usize] += 1;
        counts
    });
    counts[0] * (counts[2] + 1)
}

fn count_permutations(
    diffs: &Vec<u64>,
    cache: &mut HashMap<(usize, u64), usize>,
    i: usize,
    d: u64,
) -> usize {
    if i >= diffs.len() {
        if d == 0 {
            1
        } else {
            0
        }
    } else if diffs[i] + d > 3 {
        0
    } else if let Some(count) = cache.get(&(i, d)) {
        *count
    } else {
        // To skip or not to skip.
        let count = count_permutations(diffs, cache, i + 1, d + diffs[i])
            + count_permutations(diffs, cache, i + 1, 0);
        cache.insert((i, d), count);
        count
    }
}

fn part_02(input: &Input) -> usize {
    count_permutations(&diffs(input), &mut HashMap::new(), 0, 0)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    16
    10
    15
    5
    1
    11
    7
    19
    6
    12
    4";

    const EXAMPLE_DATA_2: &'static str = "
    28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3";

    #[test]
    fn example_1_part01() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 7 * 5);
    }

    #[test]
    fn example_2_part_01() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_01(&input), 22 * 10);
    }

    #[test]
    fn example_1_part_02() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 8);
    }

    #[test]
    fn example_2_part_02() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_02(&input), 19208);
    }
}
