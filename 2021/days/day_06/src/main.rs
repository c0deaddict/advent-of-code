use lib::run;

type Input = Vec<usize>;

fn parse_input(input: &str) -> Input {
    let mut res = vec![0; 9];
    for s in input.trim().split(",") {
        res[s.parse::<usize>().unwrap()] += 1;
    }
    return res;
}

fn simulate(input: &Input, days: usize) -> usize {
    let mut state = input.clone();

    for _ in 0..days {
        let birth = state[0];
        state.rotate_left(1);
        state[6] += birth;
        state[8] = birth;
    }

    state.iter().sum()
}

fn part_01(input: &Input) -> usize {
    simulate(input, 80)
}

fn part_02(input: &Input) -> usize {
    simulate(input, 256)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    3,4,3,1,2
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 5934)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 26984457539)
    }
}
