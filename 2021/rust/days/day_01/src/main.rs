use lib::run;

type Input = Vec<usize>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| l.parse::<usize>().unwrap())
        .collect()
}

fn part_01(input: &Input) -> usize {
    let mut increases = 0;
    for i in 1..input.len() {
        if input[i] > input[i - 1] {
            increases += 1;
        }
    }
    increases
}

fn part_02(input: &Input) -> usize {
    let mut increases = 0;
    let mut sum = input[0] + input[1] + input[2];
    for i in 3..input.len() {
        let next_sum = sum - input[i-3] + input[i];
        if next_sum > sum {
            increases += 1;
        }
        sum = next_sum;
    }
    increases
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 7)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 5)
    }
}
