use day_12::input::parse_input;
use day_12::part1::part1;
use day_12::part2::part2;
use lib::run;

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    F10
    N3
    F7
    R90
    F11";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 25);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 286);
    }
}
