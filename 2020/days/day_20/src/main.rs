use day_20::input::parse_input;
use day_20::part1::part1;
use day_20::part2::part2;
use lib::run;

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}
