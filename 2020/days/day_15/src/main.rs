use lib::run;
use std::collections::HashMap;

type Input = Vec<u64>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .split(',')
        .map(|l| l.parse().unwrap())
        .collect()
}

fn spoken_number(input: &Input, n: usize) -> u64 {
    let mut last = input[0];
    let mut spoken = HashMap::new();

    for turn in 1..n {
        let before = spoken.get(&last).cloned();
        spoken.insert(last, turn as u64 - 1);

        if turn < input.len() {
            last = input[turn];
        } else if let Some(other_turn) = before {
            last = (turn as u64 - 1) - other_turn;
        } else {
            last = 0;
        }
    }

    last
}

fn part1(input: &Input) -> u64 {
    spoken_number(input, 2020)
}

fn part2(input: &Input) -> u64 {
    spoken_number(input, 30000000)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_1_part1() {
        assert_eq!(part1(&parse_input("1,3,2")), 1);
    }

    #[test]
    fn example_2_part1() {
        assert_eq!(part1(&parse_input("2,1,3")), 10);
    }

    #[test]
    fn example_3_part1() {
        assert_eq!(part1(&parse_input("1,2,3")), 27);
    }

    #[test]
    fn example_4_part1() {
        assert_eq!(part1(&parse_input("2,3,1")), 78);
    }

    #[test]
    fn example_5_part1() {
        assert_eq!(part1(&parse_input("3,2,1")), 438);
    }

    #[test]
    fn example_6_part1() {
        assert_eq!(part1(&parse_input("3,1,2")), 1836);
    }

    #[test]
    fn example_1_part2() {
        assert_eq!(part2(&parse_input("0,3,6")), 175594);
    }

    #[test]
    fn example_2_part2() {
        assert_eq!(part2(&parse_input("1,3,2")), 2578);
    }

    #[test]
    fn example_3_part2() {
        assert_eq!(part2(&parse_input("2,1,3")), 3544142);
    }

    #[test]
    fn example_4_part2() {
        assert_eq!(part2(&parse_input("1,2,3")), 261214);
    }

    #[test]
    fn example_5_part2() {
        assert_eq!(part2(&parse_input("2,3,1")), 6895259);
    }

    #[test]
    fn example_6_part2() {
        assert_eq!(part2(&parse_input("3,2,1")), 18);
    }

    #[test]
    fn example_7_part2() {
        assert_eq!(part2(&parse_input("3,1,2")), 362);
    }
}
