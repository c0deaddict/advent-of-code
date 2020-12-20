use crate::types::*;
use crate::input::*;
use crate::part1::solve_puzzle;

pub fn part2(input: &Input) -> usize {
    let (puzzle, size) = solve_puzzle(input);
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = include_str!("example_1.txt");

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 273);
    }
}
